import socket
import ssl
import threading
from lxml import etree

class EPPConnectionLimitError(Exception):
    pass

class EPPSession:
    def __init__(self, host, port, certfile, keyfile, timeout=30):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.timeout = timeout
        self.sock = None
        self.ssl_sock = None
        self.session_active = False
        self._recv_lock = threading.Lock()

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        self.ssl_sock = context.wrap_socket(self.sock, server_hostname=self.host)
        self.session_active = True
        # Receive server greeting
        greeting = self._recv_response()
        return greeting

    def disconnect(self):
        if self.ssl_sock:
            self.ssl_sock.close()
        if self.sock:
            self.sock.close()
        self.session_active = False

    def _send_command(self, xml: str):
        data = xml.encode('utf-8')
        length = len(data) + 4
        msg = length.to_bytes(4, byteorder='big') + data
        self.ssl_sock.sendall(msg)

    def _recv_response(self) -> str:
        with self._recv_lock:
            length_bytes = self.ssl_sock.recv(4)
            if not length_bytes or len(length_bytes) < 4:
                raise ConnectionError('Failed to read EPP response length')
            length = int.from_bytes(length_bytes, byteorder='big')
            data = b''
            while len(data) < length - 4:
                chunk = self.ssl_sock.recv(length - 4 - len(data))
                if not chunk:
                    break
                data += chunk
            return data.decode('utf-8')

    def hello(self, return_xml: bool = False):
        hello_xml = self._build_hello_xml()
        self._send_command(hello_xml)
        response_xml = self._recv_response()
        if return_xml:
            return response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            svID = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}svID')
            svDate = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}svDate')
            return {
                'svID': svID.text if svID is not None else None,
                'svDate': svDate.text if svDate is not None else None
            }
        except Exception:
            return {}

    def login(self, username, password, return_xml: bool = False):
        if not self.session_active:
            self.connect()
        login_xml = self._build_login_xml(username, password)
        self._send_command(login_xml)
        response_xml = self._recv_response()
        # Parse response for connection limit info and result code
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            msg_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}msg')
            if msg_elem is not None and 'permitted connections' in msg_elem.text:
                import re
                m = re.search(r'using (\d+) out of (\d+) permitted connections', msg_elem.text)
                if m:
                    current, maximum = int(m.group(1)), int(m.group(2))
                    if current > maximum:
                        raise EPPConnectionLimitError(f"Connection limit exceeded: using {current} out of {maximum} permitted connections.")
            # Check EPP result code
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            if result_elem is not None:
                code = int(result_elem.get('code', '0'))
                if 1000 <= code < 2000:
                    return (True, response_xml) if return_xml else True
                else:
                    return (False, response_xml) if return_xml else False
        except Exception as e:
            # If parsing fails, treat as error
            if return_xml:
                return False, response_xml
            return False

    def logout(self):
        logout_xml = self._build_logout_xml()
        self._send_command(logout_xml)
        response = self._recv_response()
        self.disconnect()
        return response

    def _build_login_xml(self, username, password) -> str:
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        login = etree.SubElement(command, 'login')
        clID = etree.SubElement(login, 'clID')
        clID.text = username
        pw = etree.SubElement(login, 'pw')
        pw.text = password
        options = etree.SubElement(login, 'options')
        version = etree.SubElement(options, 'version')
        version.text = '1.0'
        lang = etree.SubElement(options, 'lang')
        lang.text = 'en'
        svcs = etree.SubElement(login, 'svcs')
        etree.SubElement(svcs, 'objURI').text = 'urn:ietf:params:xml:ns:domain-1.0'
        etree.SubElement(svcs, 'objURI').text = 'urn:ietf:params:xml:ns:contact-1.0'
        etree.SubElement(svcs, 'objURI').text = 'urn:ietf:params:xml:ns:host-1.0'
        # Always add SK-NIC extension for contact-ident
        ext = etree.SubElement(svcs, 'svcExtension')
        etree.SubElement(ext, 'extURI').text = 'http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2'
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def _build_logout_xml(self) -> str:
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        etree.SubElement(command, 'logout')
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def _build_hello_xml(self) -> str:
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        etree.SubElement(root, 'hello')
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

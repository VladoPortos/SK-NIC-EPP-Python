from lxml import etree

class EPPPoll:
    """
    Implements EPP <poll> commands for message queue management (SK-NIC and RFC 5730).
    """
    def __init__(self, client):
        self.client = client

    def poll(self, op="req", msgID=None, clTRID="ABC-12345", return_xml=False):
        """
        Perform a <poll> operation.
        op: 'req' (request next), 'ack' (acknowledge message by msgID)
        msgID: required for 'ack' operation
        """
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        poll_elem = etree.SubElement(command, 'poll')
        poll_elem.set('op', op)
        if op == 'ack' and msgID:
            poll_elem.set('msgID', str(msgID))
        etree.SubElement(command, 'clTRID').text = clTRID
        poll_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(poll_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            # Extract message queue info if present
            msgQ_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}msgQ')
            msgQ = None
            if msgQ_elem is not None:
                msgQ = {
                    'count': msgQ_elem.get('count'),
                    'id': msgQ_elem.get('id'),
                    'text': msgQ_elem.text
                }
            result = {'result_code': code, 'msg': msg, 'msgQ': msgQ}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

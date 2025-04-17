from lxml import etree

class EPPHost:
    def __init__(self, client):
        self.client = client

    def create(self, host_name, addresses=None, clTRID="ABC-12345", return_xml=False):
        """
        Create a host (nameserver). addresses: list of dicts, each {'ip': '...', 'type': 'v4' or 'v6'}
        """
        host_ns = 'urn:ietf:params:xml:ns:host-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        create = etree.SubElement(command, 'create')
        host_create = etree.SubElement(create, f'{{{host_ns}}}create', nsmap={'host': host_ns})
        etree.SubElement(host_create, f'{{{host_ns}}}name').text = host_name
        if addresses:
            for addr in addresses:
                addr_elem = etree.SubElement(host_create, f'{{{host_ns}}}addr')
                if 'type' in addr and addr['type']:
                    addr_elem.set('ip', addr['type'])
                addr_elem.text = addr['ip']
        etree.SubElement(command, 'clTRID').text = clTRID
        create_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(create_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'host': host_name, 'result_code': code, 'msg': msg}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'host': host_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def update(self, host_name, add_addrs=None, rem_addrs=None, new_name=None, clTRID="ABC-12345", return_xml=False):
        """
        Update a host (add/remove IPs or change name). add_addrs/rem_addrs: list of dicts {'ip': '...', 'type': 'v4'/'v6'}
        """
        host_ns = 'urn:ietf:params:xml:ns:host-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        update = etree.SubElement(command, 'update')
        host_update = etree.SubElement(update, f'{{{host_ns}}}update', nsmap={'host': host_ns})
        etree.SubElement(host_update, f'{{{host_ns}}}name').text = host_name
        if add_addrs:
            add = etree.SubElement(host_update, f'{{{host_ns}}}add')
            for addr in add_addrs:
                addr_elem = etree.SubElement(add, f'{{{host_ns}}}addr')
                if 'type' in addr and addr['type']:
                    addr_elem.set('ip', addr['type'])
                addr_elem.text = addr['ip']
        if rem_addrs:
            rem = etree.SubElement(host_update, f'{{{host_ns}}}rem')
            for addr in rem_addrs:
                addr_elem = etree.SubElement(rem, f'{{{host_ns}}}addr')
                if 'type' in addr and addr['type']:
                    addr_elem.set('ip', addr['type'])
                addr_elem.text = addr['ip']
        if new_name:
            chg = etree.SubElement(host_update, f'{{{host_ns}}}chg')
            etree.SubElement(chg, f'{{{host_ns}}}name').text = new_name
        etree.SubElement(command, 'clTRID').text = clTRID
        update_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(update_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'host': host_name, 'result_code': code, 'msg': msg}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'host': host_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def delete(self, host_name, clTRID="ABC-12345", return_xml=False):
        """
        Delete a host (nameserver).
        """
        host_ns = 'urn:ietf:params:xml:ns:host-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        delete = etree.SubElement(command, 'delete')
        host_delete = etree.SubElement(delete, f'{{{host_ns}}}delete', nsmap={'host': host_ns})
        etree.SubElement(host_delete, f'{{{host_ns}}}name').text = host_name
        etree.SubElement(command, 'clTRID').text = clTRID
        delete_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(delete_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'host': host_name, 'result_code': code, 'msg': msg}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'host': host_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def check(self, host_names, return_xml: bool = False):
        check_xml = self._build_check_xml(host_names)
        self.client._send_command(check_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            ns = '{urn:ietf:params:xml:ns:host-1.0}'
            results = []
            for cd in root.findall('.//' + ns + 'cd'):
                name_elem = cd.find(ns + 'name')
                reason_elem = cd.find(ns + 'reason')
                if name_elem is not None:
                    res = {
                        'name': name_elem.text,
                        'available': name_elem.get('avail') == '1'
                    }
                    if reason_elem is not None:
                        res['reason'] = reason_elem.text
                    results.append(res)
            if not results:
                # fallback for single name
                if isinstance(host_names, str):
                    results = [{'name': host_names, 'available': None}]
        except Exception:
            if isinstance(host_names, str):
                results = [{'name': host_names, 'available': None}]
            else:
                results = [{'name': n, 'available': None} for n in host_names]
        if return_xml:
            return results, response_xml
        return results if isinstance(host_names, list) else results[0]

    def _build_check_xml(self, host_names, clTRID="ABC-12345"):
        if isinstance(host_names, str):
            host_names = [host_names]
        host_ns = 'urn:ietf:params:xml:ns:host-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        check = etree.SubElement(command, 'check')
        host_check = etree.SubElement(check, f'{{{host_ns}}}check', nsmap={'host': host_ns})
        for n in host_names:
            name_elem = etree.SubElement(host_check, f'{{{host_ns}}}name')
            name_elem.text = n
        etree.SubElement(command, 'clTRID').text = clTRID
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def info(self, host_name: str, return_xml: bool = False):
        info_xml = self._build_info_xml(host_name)
        self.client._send_command(info_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            ns = '{urn:ietf:params:xml:ns:host-1.0}'
            inf_data = root.find('.//' + ns + 'infData')
            result = {'host': host_name}
            if inf_data is not None:
                name_elem = inf_data.find(ns + 'name')
                if name_elem is not None:
                    result['host'] = name_elem.text
                # Status (can be multiple)
                status_elems = inf_data.findall(ns + 'status')
                result['status'] = [e.get('s') for e in status_elems] if status_elems else None
                # Addresses (can be v4/v6)
                addresses = []
                for addr_elem in inf_data.findall(ns + 'addr'):
                    ip = addr_elem.text
                    ip_type = addr_elem.get('ip')
                    addresses.append({'ip': ip, 'type': ip_type})
                if addresses:
                    result['addresses'] = addresses
                # Registrar IDs
                for field in ['clID', 'crID', 'upID']:
                    elem = inf_data.find(ns + field)
                    if elem is not None:
                        result[field] = elem.text
                # Dates
                for field in ['crDate', 'upDate', 'trDate']:
                    elem = inf_data.find(ns + field)
                    if elem is not None:
                        result[field] = elem.text
            else:
                # fallback: at least host and status
                name_elem = root.find('.//' + ns + 'name')
                status_elem = root.find('.//' + ns + 'status')
                result['host'] = name_elem.text if name_elem is not None else host_name
                result['status'] = status_elem.get('s') if status_elem is not None else None
        except Exception:
            result = {'host': host_name, 'status': None}
        if return_xml:
            return result, response_xml
        return result

    def _build_info_xml(self, host_name, clTRID="ABC-12345"):
        host_ns = 'urn:ietf:params:xml:ns:host-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        info = etree.SubElement(command, 'info')
        host_info = etree.SubElement(info, f'{{{host_ns}}}info', nsmap={'host': host_ns})
        name_elem = etree.SubElement(host_info, f'{{{host_ns}}}name')
        name_elem.text = host_name
        etree.SubElement(command, 'clTRID').text = clTRID
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

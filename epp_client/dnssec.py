from lxml import etree

class EPPDNSSEC:
    """
    Implements DNSSEC (secDNS-1.1) extension commands for SK-NIC EPP.
    Supports add, remove, update, and info of DS records for a domain.
    """
    def __init__(self, client):
        self.client = client

    def info(self, domain_name, clTRID="ABC-DNSSEC-INFO", return_xml=False):
        """
        Query DNSSEC info (DS data) for a domain.
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        secdns_ns = 'urn:ietf:params:xml:ns:secDNS-1.1'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        info = etree.SubElement(command, 'info')
        domain_info = etree.SubElement(info, f'{{{domain_ns}}}info', nsmap={'domain': domain_ns})
        etree.SubElement(domain_info, f'{{{domain_ns}}}name').text = domain_name
        extension = etree.SubElement(command, 'extension')
        etree.SubElement(extension, f'{{{secdns_ns}}}info', nsmap={'secDNS': secdns_ns})
        etree.SubElement(command, 'clTRID').text = clTRID
        xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            # Parse DS data from response if present
            ds_data = []
            for ds in root.findall('.//{urn:ietf:params:xml:ns:secDNS-1.1}dsData'):
                ds_data.append({
                    'keyTag': ds.findtext('{urn:ietf:params:xml:ns:secDNS-1.1}keyTag'),
                    'alg': ds.findtext('{urn:ietf:params:xml:ns:secDNS-1.1}alg'),
                    'digestType': ds.findtext('{urn:ietf:params:xml:ns:secDNS-1.1}digestType'),
                    'digest': ds.findtext('{urn:ietf:params:xml:ns:secDNS-1.1}digest'),
                })
            result = {'domain': domain_name, 'ds_data': ds_data}
        except Exception as ex:
            result = {'domain': domain_name, 'ds_data': None, 'error': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def update(self, domain_name, add=None, rem=None, chg=None, clTRID="ABC-DNSSEC-UPDATE", return_xml=False):
        """
        Update DNSSEC DS records for a domain.
        add: list of DS dicts to add
        rem: list of DS dicts to remove, or 'all' to remove all
        chg: dict with 'maxSigLife' (optional)
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        secdns_ns = 'urn:ietf:params:xml:ns:secDNS-1.1'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        update = etree.SubElement(command, 'update')
        domain_update = etree.SubElement(update, f'{{{domain_ns}}}update', nsmap={'domain': domain_ns})
        etree.SubElement(domain_update, f'{{{domain_ns}}}name').text = domain_name
        extension = etree.SubElement(command, 'extension')
        secdns_update = etree.SubElement(extension, f'{{{secdns_ns}}}update', nsmap={'secDNS': secdns_ns})
        if rem:
            rem_elem = etree.SubElement(secdns_update, f'{{{secdns_ns}}}rem')
            if rem == 'all':
                etree.SubElement(rem_elem, f'{{{secdns_ns}}}all').text = 'true'
            else:
                for ds in rem:
                    ds_elem = etree.SubElement(rem_elem, f'{{{secdns_ns}}}dsData')
                    for k, v in ds.items():
                        etree.SubElement(ds_elem, f'{{{secdns_ns}}}{k}').text = str(v)
        if add:
            add_elem = etree.SubElement(secdns_update, f'{{{secdns_ns}}}add')
            for ds in add:
                ds_elem = etree.SubElement(add_elem, f'{{{secdns_ns}}}dsData')
                for k, v in ds.items():
                    etree.SubElement(ds_elem, f'{{{secdns_ns}}}{k}').text = str(v)
        if chg and 'maxSigLife' in chg:
            chg_elem = etree.SubElement(secdns_update, f'{{{secdns_ns}}}chg')
            etree.SubElement(chg_elem, f'{{{secdns_ns}}}maxSigLife').text = str(chg['maxSigLife'])
        etree.SubElement(command, 'clTRID').text = clTRID
        xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'domain': domain_name, 'result_code': code, 'msg': msg}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'domain': domain_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

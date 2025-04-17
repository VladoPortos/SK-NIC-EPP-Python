from lxml import etree

class EPPRGP:
    """
    Implements EPP RGP (Redemption Grace Period) extension commands for domain restore (RFC 3915, SK-NIC compliant).
    """
    def __init__(self, client):
        self.client = client

    def restore_request(self, domain_name, clTRID="ABC-RESTORE-1", return_xml=False):
        """
        Send <rgp:update> with <rgp:restore op="request"> to begin domain restore from redemption period.
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        rgp_ns = 'urn:ietf:params:xml:ns:rgp-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        update = etree.SubElement(command, 'update')
        domain_update = etree.SubElement(update, f'{{{domain_ns}}}update', nsmap={'domain': domain_ns})
        etree.SubElement(domain_update, f'{{{domain_ns}}}name').text = domain_name
        # Extension for RGP
        extension = etree.SubElement(command, 'extension')
        rgp_update = etree.SubElement(extension, f'{{{rgp_ns}}}update', nsmap={'rgp': rgp_ns})
        etree.SubElement(rgp_update, f'{{{rgp_ns}}}restore', op='request')
        etree.SubElement(command, 'clTRID').text = clTRID
        restore_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(restore_xml)
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

    def restore_report(self, domain_name, pre_data, post_data, del_time=None, res_time=None, res_reason=None, statements=None, other=None, clTRID="ABC-RESTORE-2", return_xml=False):
        """
        Send <rgp:update> with <rgp:restore op="report"> to submit restore report (SK-NIC/RFC3915 compliant).
        Args:
            domain_name: domain being restored
            pre_data: string, info before deletion
            post_data: string, info after restore
            del_time: deletion timestamp (ISO8601, required)
            res_time: restore timestamp (ISO8601, required)
            res_reason: reason for restore (required)
            statements: list of two statements (required)
            other: optional extra info
            clTRID: client transaction id
            return_xml: return XML as well as result dict
        """
        from datetime import datetime
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        rgp_ns = 'urn:ietf:params:xml:ns:rgp-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        update = etree.SubElement(command, 'update')
        domain_update = etree.SubElement(update, f'{{{domain_ns}}}update', nsmap={'domain': domain_ns})
        etree.SubElement(domain_update, f'{{{domain_ns}}}name').text = domain_name
        extension = etree.SubElement(command, 'extension')
        rgp_update = etree.SubElement(extension, f'{{{rgp_ns}}}update', nsmap={'rgp': rgp_ns})
        restore_elem = etree.SubElement(rgp_update, f'{{{rgp_ns}}}restore', op='report')
        report_elem = etree.SubElement(restore_elem, f'{{{rgp_ns}}}report')
        etree.SubElement(report_elem, f'{{{rgp_ns}}}preData').text = pre_data
        etree.SubElement(report_elem, f'{{{rgp_ns}}}postData').text = post_data
        # Provide sensible ISO8601 defaults if not given
        now = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
        etree.SubElement(report_elem, f'{{{rgp_ns}}}delTime').text = del_time or now
        etree.SubElement(report_elem, f'{{{rgp_ns}}}resTime').text = res_time or now
        etree.SubElement(report_elem, f'{{{rgp_ns}}}resReason').text = res_reason or "Registrant requested restore."
        stmts = statements or [
            "The information in this report is true to best of my knowledge.",
            "I have not restored this domain in bad faith."
        ]
        for stmt in stmts[:2]:
            etree.SubElement(report_elem, f'{{{rgp_ns}}}statement').text = stmt
        if other:
            etree.SubElement(report_elem, f'{{{rgp_ns}}}other').text = other
        etree.SubElement(command, 'clTRID').text = clTRID
        report_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(report_xml)
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

from lxml import etree

class EPPDomain:
    def __init__(self, client):
        self.client = client

    def create(self, domain_name, period, registrant, admin_contact, tech_contact, nameservers, auth_info_pw=None, return_xml=False, clTRID="ABC-12345"):
        """
        Create a new domain in SK-NIC EPP. Returns dict (and optionally XML).
        Minimal required: domain_name, period, registrant, admin_contact, tech_contact, nameservers, auth_info_pw
        If auth_info_pw is not provided, a secure password will be auto-generated and returned in the result.
        """
        from .utils import generate_auth_info_pw
        # Auto-generate password if not provided
        if not auth_info_pw:
            auth_info_pw = generate_auth_info_pw()
            generated_pw = True
        else:
            generated_pw = False
        # Pre-checks
        if not domain_name or not period or not registrant or not admin_contact or not tech_contact or not nameservers:
            return {'domain': domain_name, 'result_code': 'LOCAL-ERROR', 'msg': 'Missing required field.'}
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        create = etree.SubElement(command, 'create')
        domain_create = etree.SubElement(create, f'{{{domain_ns}}}create', nsmap={'domain': domain_ns})
        etree.SubElement(domain_create, f'{{{domain_ns}}}name').text = domain_name
        period_elem = etree.SubElement(domain_create, f'{{{domain_ns}}}period', unit='y')
        period_elem.text = str(period)
        ns_elem = etree.SubElement(domain_create, f'{{{domain_ns}}}ns')
        for ns in nameservers:
            etree.SubElement(ns_elem, f'{{{domain_ns}}}hostObj').text = ns
        etree.SubElement(domain_create, f'{{{domain_ns}}}registrant').text = registrant
        etree.SubElement(domain_create, f'{{{domain_ns}}}contact', type='admin').text = admin_contact
        etree.SubElement(domain_create, f'{{{domain_ns}}}contact', type='tech').text = tech_contact
        authinfo_elem = etree.SubElement(domain_create, f'{{{domain_ns}}}authInfo')
        etree.SubElement(authinfo_elem, f'{{{domain_ns}}}pw').text = auth_info_pw
        etree.SubElement(command, 'clTRID').text = clTRID
        domain_create_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(domain_create_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        # Parse result
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            cre_data = root.find('.//{urn:ietf:params:xml:ns:domain-1.0}creData')
            result = {'domain': domain_name, 'result_code': code, 'msg': msg}
            if cre_data is not None:
                id_elem = cre_data.find('{urn:ietf:params:xml:ns:domain-1.0}name')
                if id_elem is not None:
                    result['id'] = id_elem.text
                cr_date = cre_data.find('{urn:ietf:params:xml:ns:domain-1.0}crDate')
                if cr_date is not None:
                    result['crDate'] = cr_date.text
                ex_date = cre_data.find('{urn:ietf:params:xml:ns:domain-1.0}exDate')
                if ex_date is not None:
                    result['exDate'] = ex_date.text
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'domain': domain_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def delete(self, domain_name, return_xml=False, clTRID="ABC-12345"):
        """
        Delete a domain by name. Returns dict (and optionally XML).
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        delete = etree.SubElement(command, 'delete')
        domain_delete = etree.SubElement(delete, f'{{{domain_ns}}}delete', nsmap={'domain': domain_ns})
        etree.SubElement(domain_delete, f'{{{domain_ns}}}name').text = domain_name
        etree.SubElement(command, 'clTRID').text = clTRID
        domain_delete_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(domain_delete_xml)
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

    def update(self, domain_name, add_ns=None, rem_ns=None, add_contacts=None, rem_contacts=None, registrant=None, auth_info=None, return_xml=False, clTRID="ABC-12345"):
        """
        Update a domain (nameservers, contacts, registrant, authInfo) SK-NIC compliant.
        add_ns/rem_ns: list of nameservers to add/remove
        add_contacts/rem_contacts: list of dicts: {type: "admin"|"tech", id: contact_id}
        registrant: new registrant contact ID
        auth_info: new authInfo password
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        update = etree.SubElement(command, 'update')
        domain_update = etree.SubElement(update, f'{{{domain_ns}}}update', nsmap={'domain': domain_ns})
        etree.SubElement(domain_update, f'{{{domain_ns}}}name').text = domain_name
        # <add>
        if add_ns or add_contacts:
            add_elem = etree.SubElement(domain_update, f'{{{domain_ns}}}add')
            if add_ns:
                ns_elem = etree.SubElement(add_elem, f'{{{domain_ns}}}ns')
                for ns in add_ns:
                    etree.SubElement(ns_elem, f'{{{domain_ns}}}hostObj').text = ns
            if add_contacts:
                for c in add_contacts:
                    etree.SubElement(add_elem, f'{{{domain_ns}}}contact', type=c['type']).text = c['id']
        # <rem>
        if rem_ns or rem_contacts:
            rem_elem = etree.SubElement(domain_update, f'{{{domain_ns}}}rem')
            if rem_ns:
                ns_elem = etree.SubElement(rem_elem, f'{{{domain_ns}}}ns')
                for ns in rem_ns:
                    etree.SubElement(ns_elem, f'{{{domain_ns}}}hostObj').text = ns
            if rem_contacts:
                for c in rem_contacts:
                    etree.SubElement(rem_elem, f'{{{domain_ns}}}contact', type=c['type']).text = c['id']
        # <chg>
        if registrant or auth_info:
            chg_elem = etree.SubElement(domain_update, f'{{{domain_ns}}}chg')
            if registrant:
                etree.SubElement(chg_elem, f'{{{domain_ns}}}registrant').text = registrant
            if auth_info:
                authinfo_elem = etree.SubElement(chg_elem, f'{{{domain_ns}}}authInfo')
                etree.SubElement(authinfo_elem, f'{{{domain_ns}}}pw').text = auth_info
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
            result = {'domain': domain_name, 'result_code': code, 'msg': msg}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'domain': domain_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def renew(self, domain_name, cur_exp_date, period=1, return_xml=False, clTRID="ABC-12345"):
        """
        Renew a domain (extend registration period) SK-NIC compliant.
        domain_name: domain to renew
        cur_exp_date: current expiration date (YYYY-MM-DD)
        period: years to extend (default 1)
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        renew = etree.SubElement(command, 'renew')
        domain_renew = etree.SubElement(renew, f'{{{domain_ns}}}renew', nsmap={'domain': domain_ns})
        etree.SubElement(domain_renew, f'{{{domain_ns}}}name').text = domain_name
        etree.SubElement(domain_renew, f'{{{domain_ns}}}curExpDate').text = cur_exp_date
        if period:
            period_elem = etree.SubElement(domain_renew, f'{{{domain_ns}}}period', unit='y')
            period_elem.text = str(period)
        etree.SubElement(command, 'clTRID').text = clTRID
        renew_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(renew_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'domain': domain_name, 'result_code': code, 'msg': msg}
            # Try to get new exDate
            ren_data = root.find('.//{urn:ietf:params:xml:ns:domain-1.0}renData')
            if ren_data is not None:
                ex_date = ren_data.find('{urn:ietf:params:xml:ns:domain-1.0}exDate')
                if ex_date is not None:
                    result['exDate'] = ex_date.text
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'domain': domain_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def transfer(self, domain_name, auth_info, op="request", return_xml=False, clTRID="ABC-12345"):
        """
        Transfer a domain (SK-NIC EPP compliant).
        domain_name: domain to transfer
        auth_info: transfer password
        op: transfer operation (request, approve, reject, cancel, query)
        """
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        transfer = etree.SubElement(command, 'transfer', op=op)
        domain_transfer = etree.SubElement(transfer, f'{{{domain_ns}}}transfer', nsmap={'domain': domain_ns})
        etree.SubElement(domain_transfer, f'{{{domain_ns}}}name').text = domain_name
        authinfo_elem = etree.SubElement(domain_transfer, f'{{{domain_ns}}}authInfo')
        etree.SubElement(authinfo_elem, f'{{{domain_ns}}}pw').text = auth_info
        etree.SubElement(command, 'clTRID').text = clTRID
        transfer_xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(transfer_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'domain': domain_name, 'result_code': code, 'msg': msg}
            # Try to parse transfer data (trnData)
            trn_data = root.find('.//{urn:ietf:params:xml:ns:domain-1.0}trnData')
            if trn_data is not None:
                for field in ['name', 'trStatus', 'reID', 'acID', 'reDate', 'acDate', 'exDate']:
                    elem = trn_data.find(f'{{{domain_ns}}}{field}')
                    if elem is not None:
                        result[field] = elem.text
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'domain': domain_name, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def check(self, domain_names, return_xml: bool = False):
        check_xml = self._build_check_xml(domain_names)
        self.client._send_command(check_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            results = []
            for name_elem in root.findall('.//{urn:ietf:params:xml:ns:domain-1.0}name'):
                available = name_elem.get('avail') == '1'
                results.append({'domain': name_elem.text, 'available': available})
            if not results:
                # fallback for single domain
                if isinstance(domain_names, str):
                    results = [{'domain': domain_names, 'available': None}]
        except Exception:
            if isinstance(domain_names, str):
                results = [{'domain': domain_names, 'available': None}]
            else:
                results = [{'domain': d, 'available': None} for d in domain_names]
        if return_xml:
            return results, response_xml
        return results if isinstance(domain_names, list) else results[0]

    def info(self, domain_name: str, return_xml: bool = False):
        info_xml = self._build_info_xml(domain_name)
        self.client._send_command(info_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            ns = '{urn:ietf:params:xml:ns:domain-1.0}'
            inf_data = root.find('.//' + ns + 'infData')
            result = {'domain': domain_name}
            if inf_data is not None:
                name_elem = inf_data.find(ns + 'name')
                if name_elem is not None:
                    result['domain'] = name_elem.text
                # Status (can be multiple)
                status_elems = inf_data.findall(ns + 'status')
                result['status'] = [e.get('s') for e in status_elems] if status_elems else None
                # Registrant
                registrant_elem = inf_data.find(ns + 'registrant')
                if registrant_elem is not None:
                    result['registrant'] = registrant_elem.text
                # Contacts (tech, admin, billing)
                contacts = {}
                for ctype in ['tech', 'admin', 'billing']:
                    elems = inf_data.findall(ns + 'contact')
                    for elem in elems:
                        if elem.get('type') == ctype:
                            contacts.setdefault(ctype, []).append(elem.text)
                if contacts:
                    result['contacts'] = contacts
                # Nameservers
                ns_elem = inf_data.find(ns + 'ns')
                if ns_elem is not None:
                    hosts = [h.text for h in ns_elem.findall(ns + 'hostObj') if h.text]
                    if hosts:
                        result['nameservers'] = hosts
                # Registrar IDs
                for field in ['clID', 'crID', 'upID']:
                    elem = inf_data.find(ns + field)
                    if elem is not None:
                        result[field] = elem.text
                # Dates
                for field in ['crDate', 'upDate', 'exDate', 'trDate']:
                    elem = inf_data.find(ns + field)
                    if elem is not None:
                        result[field] = elem.text
            else:
                # fallback: at least domain and status
                name_elem = root.find('.//' + ns + 'name')
                status_elem = root.find('.//' + ns + 'status')
                result['domain'] = name_elem.text if name_elem is not None else domain_name
                result['status'] = status_elem.get('s') if status_elem is not None else None
        except Exception:
            result = {'domain': domain_name, 'status': None}
        if return_xml:
            return result, response_xml
        return result

    def _build_check_xml(self, domain_names, clTRID="ABC-12345"):
        if isinstance(domain_names, str):
            domain_names = [domain_names]
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        check = etree.SubElement(command, 'check')
        domain_check = etree.SubElement(check, f'{{{domain_ns}}}check', nsmap={'domain': domain_ns})
        for name in domain_names:
            name_elem = etree.SubElement(domain_check, f'{{{domain_ns}}}name')
            name_elem.text = name
        etree.SubElement(command, 'clTRID').text = clTRID
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def _build_info_xml(self, domain_name, clTRID="ABC-12345"):
        domain_ns = 'urn:ietf:params:xml:ns:domain-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        info = etree.SubElement(command, 'info')
        domain_info = etree.SubElement(info, f'{{{domain_ns}}}info', nsmap={'domain': domain_ns})
        name_elem = etree.SubElement(domain_info, f'{{{domain_ns}}}name')
        name_elem.text = domain_name
        etree.SubElement(command, 'clTRID').text = clTRID
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

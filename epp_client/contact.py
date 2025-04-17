from lxml import etree

class EPPContact:
    def __init__(self, client):
        self.client = client

    def create(self, contact_id, name, org, street, city, pc, cc, voice, email, auth_info_pw=None, legal_form=None,
               ident_value=None, sp=None, fax=None, disclose=None, birth_date=None, return_xml=False, clTRID="ABC-12345"):
        """
        Create a new contact in SK-NIC EPP. Returns dict (and optionally XML).
        SK-NIC Contact Identification Extension:
        - legal_form: Required. Must be 'PERS' (individual) or 'CORP' (legal entity).
        - If legal_form == 'CORP': ident_value is required, birth_date must NOT be set.
        - If legal_form == 'PERS': birth_date is recommended, ident_value must NOT be set.
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
        if not contact_id or not name or not street or not city or not pc or not cc or not voice or not email or not auth_info_pw or not legal_form:
            return {'contact_id': contact_id, 'result_code': 'LOCAL-ERROR', 'msg': 'Missing required field.'}
        SKNIC_LEGAL_FORMS = {"PERS", "CORP"}
        if legal_form not in SKNIC_LEGAL_FORMS:
            return {
                'contact_id': contact_id,
                'result_code': 'LOCAL-ERROR',
                'msg': f'legal_form must be one of {SKNIC_LEGAL_FORMS}',
                'error': f'legal_form must be one of {SKNIC_LEGAL_FORMS}'
            }
        if legal_form == "CORP":
            if not ident_value:
                return {
                    'contact_id': contact_id,
                    'result_code': 'LOCAL-ERROR',
                    'msg': 'ident_value is required for legal_form=CORP',
                    'error': 'ident_value is required for legal_form=CORP'
                }
            if birth_date:
                return {
                    'contact_id': contact_id,
                    'result_code': 'LOCAL-ERROR',
                    'msg': 'birth_date must not be set for legal_form=CORP',
                    'error': 'birth_date must not be set for legal_form=CORP'
                }
        if legal_form == "PERS":
            if ident_value:
                return {
                    'contact_id': contact_id,
                    'result_code': 'LOCAL-ERROR',
                    'msg': 'ident_value must not be set for legal_form=PERS',
                    'error': 'ident_value must not be set for legal_form=PERS'
                }
        if not auth_info_pw or len(auth_info_pw) < 16:
            return {
                'contact_id': contact_id,
                'result_code': 'LOCAL-ERROR',
                'msg': 'authInfo password must be at least 16 characters.',
                'error': 'authInfo password must be at least 16 characters.'
            }
        if not any(not c.isalnum() for c in auth_info_pw):
            return {
                'contact_id': contact_id,
                'result_code': 'LOCAL-ERROR',
                'msg': 'authInfo password must contain at least one non-alphanumeric character.',
                'error': 'authInfo password must contain at least one non-alphanumeric character.'
            }
        contact_ns = 'urn:ietf:params:xml:ns:contact-1.0'
        ext_ns = 'http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        create = etree.SubElement(command, 'create')
        contact_create = etree.SubElement(create, f'{{{contact_ns}}}create', nsmap={'contact': contact_ns})
        etree.SubElement(contact_create, f'{{{contact_ns}}}id').text = contact_id
        postal_info = etree.SubElement(contact_create, f'{{{contact_ns}}}postalInfo', type="int")
        etree.SubElement(postal_info, f'{{{contact_ns}}}name').text = name
        if org:
            etree.SubElement(postal_info, f'{{{contact_ns}}}org').text = org
        addr = etree.SubElement(postal_info, f'{{{contact_ns}}}addr')
        for s in (street if isinstance(street, list) else [street]):
            etree.SubElement(addr, f'{{{contact_ns}}}street').text = s
        etree.SubElement(addr, f'{{{contact_ns}}}city').text = city
        if sp:
            etree.SubElement(addr, f'{{{contact_ns}}}sp').text = sp
        etree.SubElement(addr, f'{{{contact_ns}}}pc').text = pc
        etree.SubElement(addr, f'{{{contact_ns}}}cc').text = cc
        etree.SubElement(contact_create, f'{{{contact_ns}}}voice').text = voice
        if fax:
            etree.SubElement(contact_create, f'{{{contact_ns}}}fax').text = fax
        etree.SubElement(contact_create, f'{{{contact_ns}}}email').text = email
        auth_info = etree.SubElement(contact_create, f'{{{contact_ns}}}authInfo')
        etree.SubElement(auth_info, f'{{{contact_ns}}}pw').text = auth_info_pw
        if disclose is not None:
            disclose_elem = etree.SubElement(contact_create, f'{{{contact_ns}}}disclose', flag=str(int(bool(disclose))))
            if isinstance(disclose, dict):
                for k in disclose:
                    etree.SubElement(disclose_elem, f'{{{contact_ns}}}{k}')
        # Extension for SK-NIC legal form/ident
        extension = etree.SubElement(command, 'extension')
        ext_create = etree.SubElement(extension, f'{{{ext_ns}}}create', nsmap={'skContactIdent': ext_ns})
        etree.SubElement(ext_create, f'{{{ext_ns}}}legalForm').text = legal_form
        if birth_date:
            etree.SubElement(ext_create, f'{{{ext_ns}}}birthDate').text = birth_date
        if ident_value:
            ident_val = etree.SubElement(ext_create, f'{{{ext_ns}}}identValue')
            etree.SubElement(ident_val, f'{{{ext_ns}}}corpIdent').text = ident_value
        etree.SubElement(command, 'clTRID').text = clTRID
        xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        # Parse response
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            ns = '{urn:ietf:params:xml:ns:contact-1.0}'
            cre_data = root.find('.//' + ns + 'creData')
            # Always parse <result> code and msg
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'contact_id': contact_id, 'result_code': code, 'msg': msg}
            if cre_data is not None:
                id_elem = cre_data.find(ns + 'id')
                if id_elem is not None:
                    result['id'] = id_elem.text
                cr_date = cre_data.find(ns + 'crDate')
                if cr_date is not None:
                    result['crDate'] = cr_date.text
            # If not success, surface error
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'contact_id': contact_id, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def check_and_create(self, contact_id, **kwargs):
        """
        Helper: Check if contact exists, create if not. Returns dict with status.
        """
        chk = self.check(contact_id)
        if isinstance(chk, list):
            chk = chk[0]
        if chk.get('available') is True:
            return self.create(contact_id, **kwargs)
        else:
            return {'contact_id': contact_id, 'status': 'already exists'}

    def delete(self, contact_id, return_xml=False, clTRID="ABC-12345"):
        """
        Delete a contact by ID. Returns dict (and optionally XML).
        """
        contact_ns = 'urn:ietf:params:xml:ns:contact-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        delete = etree.SubElement(command, 'delete')
        contact_delete = etree.SubElement(delete, f'{{{contact_ns}}}delete', nsmap={'contact': contact_ns})
        etree.SubElement(contact_delete, f'{{{contact_ns}}}id').text = contact_id
        etree.SubElement(command, 'clTRID').text = clTRID
        xml = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        self.client._send_command(xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        # Parse response
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            result_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}result')
            code = result_elem.get('code') if result_elem is not None else None
            msg_elem = result_elem.find('{urn:ietf:params:xml:ns:epp-1.0}msg') if result_elem is not None else None
            msg = msg_elem.text if msg_elem is not None else None
            result = {'contact_id': contact_id, 'result_code': code, 'msg': msg}
        except Exception:
            result = {'contact_id': contact_id, 'result_code': None, 'msg': None}
        if return_xml:
            return result, response_xml
        return result

    def update(self, contact_id, name=None, org=None, street=None, city=None, pc=None, cc=None, voice=None, email=None, fax=None, auth_info_pw=None, disclose=None, sp=None, legal_form=None, ident_value=None, birth_date=None, return_xml=False, clTRID="ABC-12345"):
        """
        Update a contact (SK-NIC EPP compliant).
        SK-NIC Contact Identification Extension:
        - If legal_form is provided: Must be 'PERS' or 'CORP'.
        - If legal_form == 'CORP': ident_value is required, birth_date must NOT be set.
        - If legal_form == 'PERS': birth_date is recommended, ident_value must NOT be set.
        All fields are optional except contact_id. Changed fields go into <contact:chg>.
        If any address field is updated, always send the complete address block by fetching missing fields from current info.
        """
        SKNIC_LEGAL_FORMS = {"PERS", "CORP"}
        if legal_form:
            if legal_form not in SKNIC_LEGAL_FORMS:
                return {
                    'contact_id': contact_id,
                    'result_code': 'LOCAL-ERROR',
                    'msg': f'legal_form must be one of {SKNIC_LEGAL_FORMS}',
                    'error': f'legal_form must be one of {SKNIC_LEGAL_FORMS}'
                }
            if legal_form == "CORP":
                if not ident_value:
                    return {
                        'contact_id': contact_id,
                        'result_code': 'LOCAL-ERROR',
                        'msg': 'ident_value is required for legal_form=CORP',
                        'error': 'ident_value is required for legal_form=CORP'
                    }
                if birth_date:
                    return {
                        'contact_id': contact_id,
                        'result_code': 'LOCAL-ERROR',
                        'msg': 'birth_date must not be set for legal_form=CORP',
                        'error': 'birth_date must not be set for legal_form=CORP'
                    }
            if legal_form == "PERS":
                if ident_value:
                    return {
                        'contact_id': contact_id,
                        'result_code': 'LOCAL-ERROR',
                        'msg': 'ident_value must not be set for legal_form=PERS',
                        'error': 'ident_value must not be set for legal_form=PERS'
                    }
        contact_ns = 'urn:ietf:params:xml:ns:contact-1.0'
        ext_ns = 'http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        update = etree.SubElement(command, 'update')
        contact_update = etree.SubElement(update, f'{{{contact_ns}}}update', nsmap={'contact': contact_ns})
        etree.SubElement(contact_update, f'{{{contact_ns}}}id').text = contact_id
        # <contact:add> and <contact:rem> are not used for SK-NIC (status only, not supported)
        # <contact:chg> for actual changes
        chg = etree.SubElement(contact_update, f'{{{contact_ns}}}chg')
        # --- PATCH: Always send full address if any address field is being updated ---
        address_fields = [street, city, pc, cc, sp]
        if any(f is not None for f in address_fields) or name is not None or org is not None:
            # Fetch current info if needed
            current = None
            if any(f is None for f in [street, city, pc, cc]):
                info = self.info(contact_id)
                # Try to get current address fields from info (if present)
                # NOTE: info() may need to be extended to return these fields if not already
                current = info.get('postalInfo', {}) if 'postalInfo' in info else {}
            # Compose new postalInfo
            postal_info = etree.SubElement(chg, f'{{{contact_ns}}}postalInfo', type="int")
            # Name
            if name is not None:
                etree.SubElement(postal_info, f'{{{contact_ns}}}name').text = name
            elif current and 'name' in current:
                etree.SubElement(postal_info, f'{{{contact_ns}}}name').text = current['name']
            # Org
            if org is not None:
                etree.SubElement(postal_info, f'{{{contact_ns}}}org').text = org
            elif current and 'org' in current:
                etree.SubElement(postal_info, f'{{{contact_ns}}}org').text = current['org']
            # Address
            addr = etree.SubElement(postal_info, f'{{{contact_ns}}}addr')
            # Street
            street_val = street if street is not None else (current.get('street') if current else None)
            if street_val:
                for s in (street_val if isinstance(street_val, list) else [street_val]):
                    etree.SubElement(addr, f'{{{contact_ns}}}street').text = s
            # City
            city_val = city if city is not None else (current.get('city') if current else None)
            if city_val:
                etree.SubElement(addr, f'{{{contact_ns}}}city').text = city_val
            # State/Province
            sp_val = sp if sp is not None else (current.get('sp') if current else None)
            if sp_val:
                etree.SubElement(addr, f'{{{contact_ns}}}sp').text = sp_val
            # Postal Code
            pc_val = pc if pc is not None else (current.get('pc') if current else None)
            if pc_val:
                etree.SubElement(addr, f'{{{contact_ns}}}pc').text = pc_val
            # Country Code
            cc_val = cc if cc is not None else (current.get('cc') if current else None)
            if cc_val:
                etree.SubElement(addr, f'{{{contact_ns}}}cc').text = cc_val
        if voice:
            etree.SubElement(chg, f'{{{contact_ns}}}voice').text = voice
        if fax:
            etree.SubElement(chg, f'{{{contact_ns}}}fax').text = fax
        if email:
            etree.SubElement(chg, f'{{{contact_ns}}}email').text = email
        if auth_info_pw:
            auth_info = etree.SubElement(chg, f'{{{contact_ns}}}authInfo')
            etree.SubElement(auth_info, f'{{{contact_ns}}}pw').text = auth_info_pw
        if disclose is not None:
            disclose_elem = etree.SubElement(chg, f'{{{contact_ns}}}disclose', flag=str(int(bool(disclose))))
            if isinstance(disclose, dict):
                for k in disclose:
                    etree.SubElement(disclose_elem, f'{{{contact_ns}}}{k}')
        # Extension for SK-NIC legal form/ident
        if legal_form or ident_value or birth_date:
            extension = etree.SubElement(command, 'extension')
            ext_update = etree.SubElement(extension, f'{{{ext_ns}}}update', nsmap={'skContactIdent': ext_ns})
            if legal_form:
                etree.SubElement(ext_update, f'{{{ext_ns}}}legalForm').text = legal_form
            if birth_date:
                etree.SubElement(ext_update, f'{{{ext_ns}}}birthDate').text = birth_date
            if ident_value:
                ident_val = etree.SubElement(ext_update, f'{{{ext_ns}}}identValue')
                etree.SubElement(ident_val, f'{{{ext_ns}}}corpIdent').text = ident_value
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
            result = {'contact_id': contact_id, 'result_code': code, 'msg': msg}
            if code and code != '1000':
                result['error'] = msg
        except Exception as ex:
            result = {'contact_id': contact_id, 'result_code': None, 'msg': str(ex)}
        if return_xml:
            return result, response_xml
        return result

    def check(self, contact_ids, return_xml: bool = False):
        check_xml = self._build_check_xml(contact_ids)
        self.client._send_command(check_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            ns = '{urn:ietf:params:xml:ns:contact-1.0}'
            results = []
            for cd in root.findall('.//' + ns + 'cd'):
                id_elem = cd.find(ns + 'id')
                reason_elem = cd.find(ns + 'reason')
                if id_elem is not None:
                    res = {
                        'id': id_elem.text,
                        'available': id_elem.get('avail') == '1'
                    }
                    if reason_elem is not None:
                        res['reason'] = reason_elem.text
                    results.append(res)
            if not results:
                # fallback for single id
                if isinstance(contact_ids, str):
                    results = [{'id': contact_ids, 'available': None}]
        except Exception:
            if isinstance(contact_ids, str):
                results = [{'id': contact_ids, 'available': None}]
            else:
                results = [{'id': cid, 'available': None} for cid in contact_ids]
        if return_xml:
            return results, response_xml
        return results if isinstance(contact_ids, list) else results[0]

    def _build_check_xml(self, contact_ids, clTRID="ABC-12345"):
        if isinstance(contact_ids, str):
            contact_ids = [contact_ids]
        contact_ns = 'urn:ietf:params:xml:ns:contact-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        check = etree.SubElement(command, 'check')
        contact_check = etree.SubElement(check, f'{{{contact_ns}}}check', nsmap={'contact': contact_ns})
        for cid in contact_ids:
            id_elem = etree.SubElement(contact_check, f'{{{contact_ns}}}id')
            id_elem.text = cid
        etree.SubElement(command, 'clTRID').text = clTRID
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def info(self, contact_id: str, return_xml: bool = False):
        info_xml = self._build_info_xml(contact_id)
        self.client._send_command(info_xml)
        response_xml = self.client._recv_response()
        self.client.last_response_xml = response_xml
        try:
            root = etree.fromstring(response_xml.encode('utf-8'))
            ns = '{urn:ietf:params:xml:ns:contact-1.0}'
            inf_data = root.find('.//' + ns + 'infData')
            result = {'contact_id': contact_id}
            if inf_data is not None:
                id_elem = inf_data.find(ns + 'id')
                if id_elem is not None:
                    result['id'] = id_elem.text
                status_elems = inf_data.findall(ns + 'status')
                result['status'] = [e.get('s') for e in status_elems] if status_elems else None
                for field in ['roid', 'clID', 'crID', 'upID', 'crDate', 'upDate', 'trDate']:
                    elem = inf_data.find(ns + field)
                    if elem is not None:
                        result[field] = elem.text
                # --- Extract postalInfo ---
                postal_info_elem = inf_data.find(ns + 'postalInfo')
                if postal_info_elem is not None:
                    postal = {}
                    name_elem = postal_info_elem.find(ns + 'name')
                    if name_elem is not None:
                        postal['name'] = name_elem.text
                    org_elem = postal_info_elem.find(ns + 'org')
                    if org_elem is not None:
                        postal['org'] = org_elem.text
                    addr_elem = postal_info_elem.find(ns + 'addr')
                    if addr_elem is not None:
                        street_elems = addr_elem.findall(ns + 'street')
                        if street_elems:
                            postal['street'] = [e.text for e in street_elems if e.text]
                        city_elem = addr_elem.find(ns + 'city')
                        if city_elem is not None:
                            postal['city'] = city_elem.text
                        sp_elem = addr_elem.find(ns + 'sp')
                        if sp_elem is not None:
                            postal['sp'] = sp_elem.text
                        pc_elem = addr_elem.find(ns + 'pc')
                        if pc_elem is not None:
                            postal['pc'] = pc_elem.text
                        cc_elem = addr_elem.find(ns + 'cc')
                        if cc_elem is not None:
                            postal['cc'] = cc_elem.text
                    result['postalInfo'] = postal
            else:
                id_elem = root.find('.//' + ns + 'id')
                status_elem = root.find('.//' + ns + 'status')
                result['id'] = id_elem.text if id_elem is not None else contact_id
                result['status'] = status_elem.get('s') if status_elem is not None else None
        except Exception:
            result = {'contact_id': contact_id, 'id': contact_id, 'status': None}
        if return_xml:
            return result, response_xml
        return result

    def _build_info_xml(self, contact_id, clTRID="ABC-12345"):
        contact_ns = 'urn:ietf:params:xml:ns:contact-1.0'
        root = etree.Element('epp', xmlns='urn:ietf:params:xml:ns:epp-1.0')
        command = etree.SubElement(root, 'command')
        info = etree.SubElement(command, 'info')
        contact_info = etree.SubElement(info, f'{{{contact_ns}}}info', nsmap={'contact': contact_ns})
        id_elem = etree.SubElement(contact_info, f'{{{contact_ns}}}id')
        id_elem.text = contact_id
        etree.SubElement(command, 'clTRID').text = clTRID
        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

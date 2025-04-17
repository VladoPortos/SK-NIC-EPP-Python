from .session import EPPSession
from .domain import EPPDomain
from .contact import EPPContact
from .host import EPPHost
from .poll import EPPPoll
from .rgp import EPPRGP
from .dnssec import EPPDNSSEC

class EPPClient:
    def __init__(self, host, port, username, password, certfile, keyfile, timeout=30):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.certfile = certfile
        self.keyfile = keyfile
        self.timeout = timeout
        self.session = EPPSession(host, port, certfile, keyfile, timeout)
        self.domain = EPPDomain(self)
        self.contact = EPPContact(self)
        self.host = EPPHost(self)
        self.poll = EPPPoll(self)
        self.rgp = EPPRGP(self)
        self.dnssec = EPPDNSSEC(self)

    def connect(self):
        return self.session.connect()

    def disconnect(self):
        return self.session.disconnect()

    def login(self, return_xml: bool = False):
        return self.session.login(self.username, self.password, return_xml=return_xml)

    def logout(self):
        return self.session.logout()

    def _send_command(self, xml: str):
        return self.session._send_command(xml)

    def _recv_response(self) -> str:
        return self.session._recv_response()

    def check_domain(self, domain_names, return_xml: bool = False):
        return self.domain.check(domain_names, return_xml=return_xml)

    def info_domain(self, domain_name: str, return_xml: bool = False):
        return self.domain.info(domain_name, return_xml=return_xml)

    def info_contact(self, contact_id: str, return_xml: bool = False):
        return self.contact.info(contact_id, return_xml=return_xml)

    def check_contact(self, contact_ids, return_xml: bool = False):
        return self.contact.check(contact_ids, return_xml=return_xml)

    def info_host(self, host_name: str, return_xml: bool = False):
        return self.host.info(host_name, return_xml=return_xml)

    def check_host(self, host_names, return_xml: bool = False):
        return self.host.check(host_names, return_xml=return_xml)

    def create_host(self, host_name, addresses=None, return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for creating a host (nameserver).
        addresses: list of dicts, each {'ip': '...', 'type': 'v4' or 'v6'}
        """
        return self.host.create(host_name, addresses=addresses, return_xml=return_xml, clTRID=clTRID)

    def update_host(self, host_name, add_addrs=None, rem_addrs=None, new_name=None, return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for updating a host (add/rem IPs or change name).
        add_addrs/rem_addrs: list of dicts {'ip': '...', 'type': 'v4'/'v6'}
        """
        return self.host.update(host_name, add_addrs=add_addrs, rem_addrs=rem_addrs, new_name=new_name, return_xml=return_xml, clTRID=clTRID)

    def delete_host(self, host_name, return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for deleting a host (nameserver).
        """
        return self.host.delete(host_name, return_xml=return_xml, clTRID=clTRID)

    def hello(self, return_xml: bool = False):
        return self.session.hello(return_xml=return_xml)
    def create_contact(self, contact_id, name, org, street, city, pc, cc, voice, email, auth_info_pw, legal_form,
                      ident_value=None, sp=None, fax=None, disclose=None, birth_date=None, return_xml=False, clTRID="ABC-12345"):
        return self.contact.create(contact_id, name, org, street, city, pc, cc, voice, email, auth_info_pw, legal_form,
                                  ident_value=ident_value, sp=sp, fax=fax, disclose=disclose, birth_date=birth_date, return_xml=return_xml, clTRID=clTRID)

    def check_and_create_contact(self, contact_id, **kwargs):
        return self.contact.check_and_create(contact_id, **kwargs)

    def delete_contact(self, contact_id, return_xml=False, clTRID="ABC-12345"):
        return self.contact.delete(contact_id, return_xml=return_xml, clTRID=clTRID)

    def create_domain(self, domain_name, period, registrant, admin_contact, tech_contact, nameservers, auth_info_pw, return_xml=False, clTRID="ABC-12345"):
        return self.domain.create(domain_name, period, registrant, admin_contact, tech_contact, nameservers, auth_info_pw, return_xml=return_xml, clTRID=clTRID)

    def delete_domain(self, domain_name, return_xml=False, clTRID="ABC-12345"):
        return self.domain.delete(domain_name, return_xml=return_xml, clTRID=clTRID)

    def update_domain(self, domain_name, add_ns=None, rem_ns=None, add_contacts=None, rem_contacts=None, registrant=None, auth_info=None, return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for updating a domain. Delegates to EPPDomain.update.
        """
        return self.domain.update(
            domain_name,
            add_ns=add_ns,
            rem_ns=rem_ns,
            add_contacts=add_contacts,
            rem_contacts=rem_contacts,
            registrant=registrant,
            auth_info=auth_info,
            return_xml=return_xml,
            clTRID=clTRID
        )

    def dnssec_info(self, domain_name, return_xml=False, clTRID="ABC-DNSSEC-INFO"):
        """
        High-level API for DNSSEC info (DS data) for a domain.
        """
        return self.dnssec.info(domain_name, clTRID=clTRID, return_xml=return_xml)

    def dnssec_update(self, domain_name, add=None, rem=None, chg=None, return_xml=False, clTRID="ABC-DNSSEC-UPDATE"):
        """
        High-level API for updating DNSSEC DS records for a domain.
        add: list of DS dicts to add
        rem: list of DS dicts to remove, or 'all' to remove all
        chg: dict with 'maxSigLife' (optional)
        """
        return self.dnssec.update(domain_name, add=add, rem=rem, chg=chg, clTRID=clTRID, return_xml=return_xml)

    def restore_domain_request(self, domain_name, return_xml=False, clTRID="ABC-RESTORE-1"):
        """
        High-level API for sending RGP restore request (begin restore from redemption period).
        """
        return self.rgp.restore_request(domain_name, clTRID=clTRID, return_xml=return_xml)

    def restore_domain_report(self, domain_name, pre_data, post_data, del_time=None, res_time=None, res_reason=None, statements=None, other=None, return_xml=False, clTRID="ABC-RESTORE-2"):
        """
        High-level API for submitting RGP restore report (after manual review).
        Passes all arguments through to EPPRGP.restore_report.
        """
        return self.rgp.restore_report(
            domain_name,
            pre_data,
            post_data,
            del_time=del_time,
            res_time=res_time,
            res_reason=res_reason,
            statements=statements,
            other=other,
            clTRID=clTRID,
            return_xml=return_xml
        )

    def restore_domain_minimal(self, domain_name, return_xml=False, clTRID="ABC-RESTORE-MIN"):
        """
        High-level API for restoring a domain with minimal input: only domain_name required.
        All RGP report fields are filled with sensible defaults and current timestamps.
        """
        # Optionally fetch info for pre/post data, but here use demo values
        pre_data = f"Domain {domain_name} info before deletion (auto)"
        post_data = f"Domain {domain_name} info after restore (auto)"
        from datetime import datetime
        now = datetime.now().replace(microsecond=0).isoformat() + 'Z'
        del_time = now
        res_time = now
        res_reason = "Registrant requested restore and provided documentation."
        statements = [
            "The information in this report is true to best of my knowledge.",
            "I have not restored this domain in bad faith."
        ]
        other = "Auto-generated restore report."
        return self.rgp.restore_report(
            domain_name,
            pre_data,
            post_data,
            del_time=del_time,
            res_time=res_time,
            res_reason=res_reason,
            statements=statements,
            other=other,
            clTRID=clTRID,
            return_xml=return_xml
        )

    def renew_domain(self, domain_name, cur_exp_date, period=1, return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for renewing a domain. Delegates to EPPDomain.renew.
        """
        return self.domain.renew(
            domain_name,
            cur_exp_date=cur_exp_date,
            period=period,
            return_xml=return_xml,
            clTRID=clTRID
        )

    def transfer_domain(self, domain_name, auth_info, op="request", return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for domain transfer. Delegates to EPPDomain.transfer.
        """
        return self.domain.transfer(
            domain_name=domain_name,
            auth_info=auth_info,
            op=op,
            return_xml=return_xml,
            clTRID=clTRID
        )

    def update_contact(self, contact_id, name=None, org=None, street=None, city=None, pc=None, cc=None, voice=None, email=None, fax=None, auth_info_pw=None, disclose=None, sp=None, legal_form=None, ident_value=None, birth_date=None, return_xml=False, clTRID="ABC-12345"):
        """
        High-level API for updating a contact. Delegates to EPPContact.update.
        """
        return self.contact.update(
            contact_id=contact_id,
            name=name,
            org=org,
            street=street,
            city=city,
            pc=pc,
            cc=cc,
            voice=voice,
            email=email,
            fax=fax,
            auth_info_pw=auth_info_pw,
            disclose=disclose,
            sp=sp,
            legal_form=legal_form,
            ident_value=ident_value,
            birth_date=birth_date,
            return_xml=return_xml,
            clTRID=clTRID
        )

    # --- POLL COMMANDS ---
    def poll_request(self, return_xml=False):
        """Request the next message in the poll queue."""
        return self.poll.poll(op="req", return_xml=return_xml)

    def poll_ack(self, msgID, return_xml=False):
        """Acknowledge a poll message by its msgID."""
        return self.poll.poll(op="ack", msgID=msgID, return_xml=return_xml)

    # More methods for check, info, create will be added here

# EPP Command Implementation Checklist

## Session Commands
- [x] `<login>` (login to EPP server)
- [x] `<logout>`
- [x] `<hello>` (server greeting)

## Domain Object Commands
- [x] `<check>` (domain availability)
- [x] `<info>` (domain info)
- [x] `<create>` (register domain)
- [x] `<update>` (modify domain)
- [x] `<delete>` (remove domain)
- [x] `<renew>` (renew domain)
- [x] `<transfer>` (domain transfer)

## Contact Object Commands
- [x] <check> (contact ID availability)
- [x] <info> (contact info)
- [x] <create> (create contact)
- [x] <update> (modify contact)
- [x] <delete> (remove contact)

## Host Object Commands
- [x] <check> (host availability)
- [x] <info> (host info)
- [x] <create> (create host)
- [x] <update> (modify host)
- [x] <delete> (remove host)

## Other Commands
- [x] <poll> (message queue)
- [x] DNSSEC extensions
  - Implemented DNSSEC info and update methods (secDNS-1.1)
  - High-level API for DS record management
  - SK-NIC XML schema compliance
  - Demo and integration ready
- [x] Contact identification extension (sk-contact-ident)
  _Implemented with full SK-NIC validation: legal_form (PERS/CORP), required ident_value and birth_date logic, and error handling for invalid combinations._
- [x] Redemption/restore (RGP) extensions
  - Implemented restore_request and restore_report methods
  - Integrated RGP demo into main.py
  - High-level API supports minimal input (just domain name) for restore
  - SK-NIC XML schema compliance confirmed
  - Note: RGP flows implemented, tested, and demoed with minimal user interaction

---

**Legend:**
- [x] Implemented in `epp_client/client.py`
- [ ] Not yet implemented

This checklist is generated based on the current implementation in `client.py` and the SK-NIC EPP command set. Update this file as you add more commands or complete implementations.

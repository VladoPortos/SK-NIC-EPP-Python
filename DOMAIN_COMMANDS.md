# Domain Object Commands

This section covers all EPP commands for managing domains: check, info, create, update, delete, renew, and transfer.

## Overview
Domain commands allow you to register, update, delete, renew, and transfer domains, as well as check availability and retrieve domain info. All SK-NIC-specific requirements (contact ident, DNSSEC, RGP, etc.) are supported.

## Supported Commands
- `<check>`: Check domain availability
- `<info>`: Get domain information
- `<create>`: Register a new domain
- `<update>`: Modify domain details (contacts, nameservers, DNSSEC, etc.)
- `<delete>`: Delete a domain
- `<renew>`: Renew a domain
- `<transfer>`: Transfer a domain between registrars

## High-Level API Usage
All domain commands are accessible via the `EPPClient` class:

# Check domain availability

```python
result = client.check_domain("example.sk")
```

# Get domain info

```python
result = client.info_domain("example.sk")
```

# Register a domain

```python
result = client.create_domain(
    domain_name="example.sk",
    period=1,
    registrant="CONTACT-ID",
    admin_contact="CONTACT-ID",
    tech_contact="CONTACT-ID",
    nameservers=["ns1.example.net", "ns2.example.net"],
    auth_info_pw="securePW123"
)
```


### Domain auth_info_pw requirements
- **Length:** 8 to 16 characters (recommended by SK-NIC)
- **Allowed characters:** Letters, numbers, and special characters (e.g. `!@#$%^&*`)
- **Security:** Should be unique per domain, not easily guessable, and stored securely.
- **Usage:** Required for domain create, transfer, and can be updated via domain update.
- **Auto-generation:** If omitted or None, a secure password will be auto-generated and returned in the result (see below).
- **Example:** `TestDomainAuth!123456`

#### Example: Auto-generate domain password

```python
result = client.create_domain(
    domain_name="example.sk",
    period=1,
    registrant="CONTACT-ID",
    admin_contact="CONTACT-ID",
    tech_contact="CONTACT-ID",
    nameservers=["ns1.example.net", "ns2.example.net"]
    # auth_info_pw omitted
)
print("New domain password:", result.get("auth_info_pw"))
```

# Update domain (add/remove nameservers, contacts, etc.)

```python
result = client.update_domain(
    domain_name="example.sk",
    add_ns=["ns3.example.net"],
    rem_ns=["ns2.example.net"]
)
```

# Delete a domain

```python
result = client.delete_domain("example.sk")
```

# Renew a domain

```python
result = client.renew_domain("example.sk", cur_exp_date="2025-01-01", period=1)
```

# Transfer a domain

```python
result = client.transfer_domain("example.sk", auth_info="securePW123", op="request")
```

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.create_domain(..., return_xml=True)
```

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

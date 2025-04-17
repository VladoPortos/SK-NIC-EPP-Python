# Contact Identification Extension (sk-contact-ident)

This section documents the SK-NIC-specific contact identification extension, which is required for all contacts in the .sk namespace.

## Overview
SK-NIC requires additional identification information for contacts, including legal form, identification value, and birth date. The EPP client fully supports and validates these requirements.

## Supported Fields
- `legal_form`: "PERS" (individual) or "CORP" (company)
- `ident_value`: Required for "CORP" (company)
- `birth_date`: Required for "PERS" (individual), recommended for "CORP"

## High-Level API Usage
All contact commands support the identification extension transparently:

```python
# Create a contact (SK-NIC ident extension)
result = client.create_contact(
    contact_id="NEW-TEST-001",
    name="John Doe",
    org="Example Org",
    street="123 Example St",
    city="Bratislava",
    pc="81101",
    cc="SK",
    voice="+421.900000000",
    email="john@example.com",
    auth_info_pw="TestContactAuth!123456",
    legal_form="PERS",  # or "CORP"
    ident_value="1234567890",  # required for CORP
    birth_date="1990-01-01"  # required for PERS
)
```

# Update a contact with identification info

```python
result = client.update_contact(
    contact_id="PERM-TEST-001",
    legal_form="CORP",
    ident_value="9876543210"
)
```

## Validation
- The client enforces SK-NIC rules:
  - Only "PERS" or "CORP" are allowed for `legal_form`
  - `ident_value` is required for "CORP"
  - `birth_date` is required for "PERS"
- Errors are raised if the requirements are not met.

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.create_contact(..., return_xml=True)
```

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

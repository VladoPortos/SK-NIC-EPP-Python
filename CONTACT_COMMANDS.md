# Contact Object Commands

This section covers EPP commands for managing contacts: check, info, create, update, delete. Includes SK-NIC-specific identification extension support.

## Overview
Contact commands allow you to create, update, and delete contacts, as well as check ID availability and retrieve contact info. The SK-NIC identification extension is fully supported and validated.

## Supported Commands
- `<check>`: Check contact ID availability
- `<info>`: Get contact information
- `<create>`: Create a new contact (with legal_form, ident_value, birth_date, etc.)
- `<update>`: Update contact details (with full SK-NIC validation)
- `<delete>`: Delete a contact

## High-Level API Usage
All contact commands are accessible via the `EPPClient` class:

# Check contact ID

```python
result = client.check_contact("PERM-TEST-001")
```

# Get contact info

```python
result = client.info_contact("PERM-TEST-001")
```

# Create a contact (SK-NIC ident extension)

```python
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

### Contact auth_info_pw requirements
- **Length:** 8 to 16 characters (recommended by SK-NIC)
- **Allowed characters:** Letters, numbers, and special characters (e.g. `!@#$%^&*`)
- **Security:** Should be unique per contact, not easily guessable, and stored securely.
- **Usage:** Required for contact create and can be updated via contact update.
- **Auto-generation:** If omitted or None, a secure password will be auto-generated and returned in the result (see below).
- **Example:** `TestContactAuth!123456`

#### Example: Auto-generate contact password

```python
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
    legal_form="PERS",  # or "CORP"
    # auth_info_pw omitted
)
print("New contact password:", result.get("auth_info_pw"))
```


# Update a contact

```python
result = client.update_contact(
    contact_id="PERM-TEST-001",
    name="Jane Doe"
)
```

# Delete a contact

```python
result = client.delete_contact("PERM-TEST-001")
```

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.create_contact(..., return_xml=True)
```

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

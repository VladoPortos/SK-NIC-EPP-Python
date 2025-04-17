# Session Commands

This section covers EPP session management commands: login, logout, and hello (greeting).

## Overview
Session commands establish and manage your connection to the SK-NIC EPP server. You must be logged in before issuing any object commands.

## Supported Commands
- `<login>`: Authenticate and open a session
- `<logout>`: Close the session
- `<hello>`: Retrieve server greeting

## High-Level API Usage
All session commands are accessible via the `EPPClient` class:

```python
from epp_client import EPPClient

client = EPPClient(
    host=EPP_HOST,
    port=EPP_PORT,
    username=EPP_USER,
    password=EPP_PASS,
    certfile=EPP_CERT,
    keyfile=EPP_KEY
)
```

# Connect and login

```python
client.connect()
client.login()
```

# Send hello (greeting)

```python
greeting = client.hello()
print(greeting)

# Logout
client.logout()
```

## Options
- All session methods can optionally return the raw XML response for debugging:

```python
result, xml = client.login(return_xml=True)
```

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

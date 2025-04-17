# Host Object Commands

This section covers EPP commands for managing hosts (nameservers): check, info, create, update, delete.

## Overview
Host commands allow you to create, update, and delete hosts (nameservers), as well as check host availability and retrieve host info. Both in-bailiwick and out-of-bailiwick hosts are supported (with SK-NIC restrictions).

## Supported Commands
- `<check>`: Check host availability
- `<info>`: Get host information
- `<create>`: Register a new host (with IPv4/IPv6 addresses)
- `<update>`: Update host addresses (add/remove IPs)
- `<delete>`: Delete a host

## High-Level API Usage
All host commands are accessible via the `EPPClient` class:


# Check host

```python
result = client.check_host("ns1.example.net")
```

# Get host info

```python
result = client.info_host("ns1.example.net")
```

# Create a host

```python
result = client.create_host(
    host_name="ns-demo-001.example.net",
    addresses=[{"ip": "192.0.2.1", "type": "v4"}, {"ip": "2001:db8::1", "type": "v6"}]
)
```

# Update a host (add/remove addresses)

```python
result = client.update_host(
    host_name="ns-demo-001.example.net",
    add_addresses=[{"ip": "192.0.2.2", "type": "v4"}],
    rem_addresses=[{"ip": "2001:db8::1", "type": "v6"}]
)
```

# Delete a host

```python
result = client.delete_host("ns-demo-001.example.net")
```

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.create_host(..., return_xml=True)
```

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

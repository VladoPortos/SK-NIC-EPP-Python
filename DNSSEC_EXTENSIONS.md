# DNSSEC Extensions

This section documents DNSSEC (secDNS-1.1) support in the EPP client for SK-NIC, including how to manage DS records for domains.

## Overview
SK-NIC supports DNSSEC via the secDNS-1.1 extension (RFC 5910). You can add, remove, or update DS records for domains. Only DS Data Interface is supported (keyData is accepted but ignored).

## Supported Operations
- Add DS record(s)
- Remove DS record(s) or all DS records
- Change maxSigLife (accepted but ignored by SK-NIC)
- Query DS records (info)

## High-Level API Usage
All DNSSEC operations are accessible via the `EPPClient` class:

# Query DNSSEC info (DS records)

```python
result = client.dnssec_info("example.sk")
```

# Add a DS record

```python
ds = {'keyTag': 12345, 'alg': 3, 'digestType': 1, 'digest': '49FD46E6C4B45C55D4AC'}
result = client.dnssec_update("example.sk", add=[ds])
```

# Remove a DS record

```python
result = client.dnssec_update("example.sk", rem=[ds])
```


# Remove all DS records

```python
result = client.dnssec_update("example.sk", rem='all')
```

# Change maxSigLife (optional, ignored by SK-NIC)

```python
result = client.dnssec_update("example.sk", chg={'maxSigLife': 604800})
```

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.dnssec_update(..., return_xml=True)
```

## Notes
- If no DNSSEC is present, omit the extension entirely.
- See [EPP_Commands.md](EPP_Commands.md) for SK-NIC XML examples.

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

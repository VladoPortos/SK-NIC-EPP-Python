# Redemption/Restore (RGP) Extensions

This section documents the Redemption Grace Period (RGP) extension support for restoring deleted domains.

## Overview
SK-NIC supports domain restoration via the RGP extension (RFC 3915). The EPP client allows you to request a restore and submit a restore report, fully compliant with SK-NIC and RFC requirements.

## Supported Operations
- **Restore Request**: Initiate a restore for a domain in redemption period
- **Restore Report**: Submit a report justifying the restoration (with all required fields)

## High-Level API Usage
All RGP operations are accessible via the `EPPClient` class:


# Request a restore for a domain in redemption period

```python
result = client.restore_domain_request("example.sk")
```

# Submit a restore report (minimal API, just domain name)

```python
result = client.restore_domain_minimal("example.sk")
```

# Advanced: Submit a restore report with custom data

```python
result = client.restore_domain_report(
    domain_name="example.sk",
    pre_data="PRE-DATA",
    post_data="POST-DATA",
    del_time="2025-01-01T12:00:00Z",
    res_time="2025-01-01T12:01:00Z",
    res_reason="Registrant requested restore.",
    statements=[
        "The information in this report is true to best of my knowledge.",
        "I have not restored this domain in bad faith."
    ],
    other="Additional info"
)
```

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.restore_domain_minimal("example.sk", return_xml=True)
```

## Notes
- The minimal API is recommended for most use cases; it auto-fills required fields.
- For compliance, see RFC 3915 and SK-NIC EPP documentation.

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

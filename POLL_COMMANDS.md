# Poll Commands

This section covers EPP poll commands for message queue management.

## Overview
The poll command allows you to retrieve and acknowledge messages from the EPP server message queue. This is essential for receiving notifications about domain transfers, expirations, and other asynchronous events.

## Supported Commands
- `<poll op="req">`: Request the next message from the queue
- `<poll op="ack">`: Acknowledge (remove) a message from the queue by its ID

## High-Level API Usage
All poll commands are accessible via the `EPPClient` class:


# Request the next message in the poll queue

```python
result = client.poll_req()
```

# Acknowledge a poll message by its msgID

```python
result = client.poll_ack(msgID="123456")
```

## Options
- All methods can optionally return the raw XML response for debugging:

```python
result, xml = client.poll_req(return_xml=True)
```

## See Also
- [main.py](main.py) for demo usage
- [plan.md](plan.md) for feature checklist
- [SK-NIC EPP documentation](EPP_Commands.md) for protocol details

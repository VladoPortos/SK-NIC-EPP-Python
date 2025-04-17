# SK-NIC EPP Client Module

A professional, modular Python client for the SK-NIC EPP (Extensible Provisioning Protocol) server, supporting all domain, contact, host, and extension commands required for full registrar automation.

## Features
- **Complete EPP command support:** Session, domain, contact, host, poll, DNSSEC, and RGP (restore) extensions
- **High-level API:** Simple, user-friendly methods for all operations, with optional access to raw XML
- **SK-NIC compliant:** Follows SK-NIC-specific extensions and requirements (contact ident, DNSSEC, RGP, etc.)
- **Secure:** Uses SSL/TLS, credentials via environment variables
- **Extensible:** Modular codebase, easy to add new extensions or commands
- **Demo & Examples:** See `main.py` for end-to-end demo flows


---

## ☕ Buy Me a Coffee (or a Beer!)

If you like this project and want to support my caffeine-fueled coding sessions, you can buy me a coffee (or a beer, I won't judge! 🍻) on Ko-fi:

[![Support me on Ko-fi](img/support_me_on_kofi_badge_red.png)](https://ko-fi.com/vladoportos)

Every donation helps to proofe to my wife that I'm not a complete idiot :D

---


## Quick Start
- Install dependencies from `requirements.txt`
- Configure your environment variables for EPP access (see example below)
- Run `main.py` to see a live demo of all commands

## .env File Example
Create a `.env` file in your project root with the following content:

```ini
EPP_HOST=epp.sk-nic.sk
EPP_PORT=700
EPP_USER=YOUR-REGISTRAR-ID
EPP_PASS=YOUR-SECRET-PASSWORD
EPP_CERT=path/to/your.crt
EPP_KEY=path/to/your.key
```
- **EPP_HOST**: The SK-NIC EPP server hostname
- **EPP_PORT**: The EPP server port (default: 700)
- **EPP_USER**: Your registrar/client ID
- **EPP_PASS**: Your EPP password
- **EPP_CERT**: Path to your SSL certificate file
- **EPP_KEY**: Path to your SSL private key file

## Documentation
This repository is fully documented. Each major command group and extension has its own detailed documentation file:

- [Session Commands](SESSION_COMMANDS.md)
- [Domain Object Commands](DOMAIN_COMMANDS.md)
- [Contact Object Commands](CONTACT_COMMANDS.md)
- [Host Object Commands](HOST_COMMANDS.md)
- [Poll Commands](POLL_COMMANDS.md)
- [DNSSEC Extensions](DNSSEC_EXTENSIONS.md)
- [Contact Identification Extension](CONTACT_IDENT_EXTENSION.md)
- [Redemption/Restore (RGP) Extensions](RGP_EXTENSIONS.md)

See [plan.md](plan.md) for a checklist of implemented features.

---

**For detailed usage, options, and sample code, see the linked documentation files and `main.py`.**

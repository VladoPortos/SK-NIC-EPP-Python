import os
import pytest
from epp_client import EPPClient
from epp_client.session import EPPConnectionLimitError

EPP_HOST = os.environ.get('EPP_HOST', 'epp.sk-nic.sk')
EPP_PORT = int(os.environ.get('EPP_PORT', 700))
EPP_USER = os.environ.get('EPP_USER', 'KLIN-0010')
EPP_PASS = os.environ.get('EPP_PASS', 'PPAoPX)RfjF+l!G4')
EPP_CERT = os.environ.get('EPP_CERT', 'my.crt')
EPP_KEY = os.environ.get('EPP_KEY', 'my.key')

@pytest.mark.parametrize("contact_ids", [["TEST-0001", "NEXT-0001"], ["NONEXIST-9999"]])
def test_check_contact(contact_ids):
    client = EPPClient(
        host=EPP_HOST,
        port=EPP_PORT,
        username=EPP_USER,
        password=EPP_PASS,
        certfile=EPP_CERT,
        keyfile=EPP_KEY
    )
    client.connect()
    client.login()
    try:
        results = client.check_contact(contact_ids)
        assert isinstance(results, list)
        for res in results:
            assert 'id' in res and 'available' in res
    finally:
        client.logout()

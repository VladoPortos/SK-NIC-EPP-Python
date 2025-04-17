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

@pytest.mark.network
@pytest.mark.slow
def test_logout():
    client = EPPClient(
        host=EPP_HOST,
        port=EPP_PORT,
        username=EPP_USER,
        password=EPP_PASS,
        certfile=EPP_CERT,
        keyfile=EPP_KEY
    )
    client.connect()
    try:
        login_result = client.login()
        if login_result:
            logout_resp = client.logout()
            assert logout_resp is not None
        else:
            pytest.skip('Login failed, skipping logout test.')
    except EPPConnectionLimitError:
        pytest.skip('Connection limit reached, skipping test.')

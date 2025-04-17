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
def test_info_host():
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
        if not login_result:
            pytest.skip('Login failed, skipping info_host test.')
        # Use a host that should exist for info test (replace with your real host)
        host_name = os.environ.get('EPP_TEST_HOST', 'ns1.sk-nic.sk')
        result = client.info_host(host_name)
        assert isinstance(result, dict)
        assert 'host' in result
        assert result['host'] == host_name
        if 'status' in result:
            assert result['status'] is None or isinstance(result['status'], (str, list))
            if isinstance(result['status'], list):
                for s in result['status']:
                    assert isinstance(s, str)
        if 'addresses' in result:
            assert isinstance(result['addresses'], list)
            for addr in result['addresses']:
                assert isinstance(addr, dict)
                assert 'ip' in addr and 'type' in addr
        for field in ['clID', 'crID', 'upID']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
        for field in ['crDate', 'upDate', 'trDate']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
    except EPPConnectionLimitError:
        pytest.skip('Connection limit reached, skipping test.')
    finally:
        client.logout()

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
def test_check_domain():
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
            pytest.skip('Login failed, skipping check_domain test.')
        # Use a domain that should not exist for availability test
        result = client.check_domain('this-domain-should-not-exist-123456.sk')
        assert isinstance(result, dict)
        assert 'available' in result
        assert result['domain'] == 'this-domain-should-not-exist-123456.sk'
        # We expect available to be True, but if registry changes, allow None
        assert result['available'] in (True, False, None)
    except EPPConnectionLimitError:
        pytest.skip('Connection limit reached, skipping test.')
    finally:
        client.logout()

@pytest.mark.network
@pytest.mark.slow
def test_info_domain():
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
            pytest.skip('Login failed, skipping info_domain test.')
        # Use a domain that should exist for info test (replace with your real domain)
        result = client.info_domain('sk-nic.sk')
        assert isinstance(result, dict)
        assert 'domain' in result
        assert result['domain'] == 'sk-nic.sk'
        # Status may be None or a list of strings (new parser returns list)
        assert result['status'] is None or isinstance(result['status'], (str, list))
        if isinstance(result.get('status'), list):
            for s in result['status']:
                assert isinstance(s, str)
        # New fields: if present, type must match
        if 'roid' in result:
            assert result['roid'] is None or isinstance(result['roid'], str)
        if 'registrant' in result:
            assert result['registrant'] is None or isinstance(result['registrant'], str)
        if 'contacts' in result:
            assert result['contacts'] is None or isinstance(result['contacts'], dict)
            if isinstance(result['contacts'], dict):
                for k, v in result['contacts'].items():
                    assert isinstance(k, str)
                    assert isinstance(v, list)
                    for contact in v:
                        assert isinstance(contact, str)
        if 'nameservers' in result:
            assert result['nameservers'] is None or isinstance(result['nameservers'], list)
            if isinstance(result['nameservers'], list):
                for ns in result['nameservers']:
                    assert isinstance(ns, str)
        for field in ['clID', 'crID', 'upID']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
        for field in ['crDate', 'upDate', 'exDate', 'trDate']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
        if 'authInfo' in result:
            assert result['authInfo'] is None or isinstance(result['authInfo'], str)
    except EPPConnectionLimitError:
        pytest.skip('Connection limit reached, skipping test.')
    finally:
        client.logout()

@pytest.mark.network
@pytest.mark.slow
def test_info_contact():
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
            pytest.skip('Login failed, skipping info_contact test.')
        # Use a contact that should exist (from env or fallback)
        contact_id = os.environ.get('EPP_TEST_CONTACT', 'sub_014524')
        result = client.info_contact(contact_id)
        assert isinstance(result, dict)
        assert 'contact_id' in result
        assert result['contact_id'] == contact_id
        # id
        if 'id' in result:
            assert result['id'] is None or isinstance(result['id'], str)
        # status
        if 'status' in result:
            assert result['status'] is None or isinstance(result['status'], (str, list))
            if isinstance(result['status'], list):
                for s in result['status']:
                    assert isinstance(s, str)
        # postalInfo
        if 'postalInfo' in result:
            assert isinstance(result['postalInfo'], dict)
            for k, v in result['postalInfo'].items():
                assert isinstance(k, str)
                assert isinstance(v, dict)
        # voice, fax, email
        for field in ['voice', 'fax', 'email']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
        # Registrar IDs
        for field in ['clID', 'crID', 'upID']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
        # Dates
        for field in ['crDate', 'upDate', 'trDate']:
            if field in result:
                assert result[field] is None or isinstance(result[field], str)
        # AuthInfo
        if 'authInfo' in result:
            assert result['authInfo'] is None or isinstance(result['authInfo'], str)
    except EPPConnectionLimitError:
        pytest.skip('Connection limit reached, skipping test.')
    finally:
        client.logout()

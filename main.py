from epp_client import EPPClient
from epp_client.session import EPPConnectionLimitError
import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Load credentials and connection info from info.md or environment variables
EPP_HOST = os.environ.get('EPP_HOST', 'epp.sk-nic.sk')
EPP_PORT = int(os.environ.get('EPP_PORT', 700))
EPP_USER = os.environ.get('EPP_USER', 'KLIN-xxxxx')
EPP_PASS = os.environ.get('EPP_PASS', 'xxxxx')
EPP_CERT = os.environ.get('EPP_CERT', 'my.crt')
EPP_KEY = os.environ.get('EPP_KEY', 'my.key')

DEBUG = False  # Set to True to print raw XML responses

def main():
    client = EPPClient(
        host=EPP_HOST,
        port=EPP_PORT,
        username=EPP_USER,
        password=EPP_PASS,
        certfile=EPP_CERT,
        keyfile=EPP_KEY
    )
    print("Connecting to EPP server...")
    try:
        greeting = client.connect()
        if DEBUG:
            print("Server greeting (XML):\n", greeting)
        else:
            print("Server greeting received.")
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    print("Logging in...")
    try:
        login_response = client.login()
        print("Login success.")
        if DEBUG:
            print("Login response (XML):\n", login_response)
    except Exception as e:
        print(f"Login failed: {e}")
        return

    # --- PERMANENT TEST CONTACT (used for domain registration) ---
    perm_contact_id = 'PERM-TEST-001'
    perm_contact_details = {
        'contact_id': perm_contact_id,
        'name': 'Permanent Test',
        'org': 'TestOrg',
        'street': '123 Test Street',
        'city': 'Bratislava',
        'pc': '81101',
        'cc': 'SK',
        'voice': '+421.900000000',
        'email': 'permanent@example.com',
        'auth_info_pw': 'PermTestAuth!123456',
        'legal_form': 'CORP',
        'ident_value': '9999999999',
        'sp': 'BA',
    }
    print(f"[Setup] Ensuring permanent test contact exists: {perm_contact_id}")
    check_perm = client.check_contact(perm_contact_id)
    if check_perm.get('available', True):
        result_perm = client.create_contact(**perm_contact_details)
        print(f"[Setup] Created permanent contact: {result_perm}")
    else:
        print(f"[Setup] Permanent contact already exists: {perm_contact_id}")

    # --- CONTACT UPDATE DEMO ---
    print(f"[Contact Demo] Updating contact: {perm_contact_id}")
    update_contact_result = client.update_contact(
        contact_id=perm_contact_id,
        name="Permanent Test Updated",
        street=["456 Updated Street"],
        auth_info_pw="PermTestAuth!654321NEW",
        return_xml=DEBUG
    )
    if DEBUG and isinstance(update_contact_result, tuple):
        result, xml = update_contact_result
        print("[Contact Demo] Update result:", result)
        print("[Contact Demo] Update response (XML):\n", xml)
    else:
        print(f"[Contact Demo] Update result: {update_contact_result}")

    # --- DOMAIN CREATE/DELETE DEMO using permanent contact ---
    import time
    import random
    suffix = int(time.time())
    test_domain = f"test-{suffix}.sk"
    nameservers = ["ns1.example.net", "ns2.example.net"]
    print(f"\n[Domain Demo] Registering domain: {test_domain}")
    domain_result = client.create_domain(
        domain_name=test_domain,
        period=1,
        registrant=perm_contact_id,
        admin_contact=perm_contact_id,
        tech_contact=perm_contact_id,
        nameservers=nameservers,
        auth_info_pw="TestDomainAuth!123456"
    )
    print(f"[Domain Demo] Create result: {domain_result}")
    if domain_result.get('result_code') == '1000':
        # --- DOMAIN INFO DEMO (for robust exDate) ---
        print(f"[Domain Demo] Fetching info for domain: {test_domain}")
        info_result = client.info_domain(test_domain)
        ex_date_full = None
        if isinstance(info_result, dict):
            ex_date_full = info_result.get('exDate')
        if ex_date_full:
            cur_exp_date = ex_date_full.split('T')[0]
            print(f"[Domain Demo] Renewing domain: {test_domain} (exp date from info: {cur_exp_date})")
            renew_result = client.renew_domain(
                domain_name=test_domain,
                cur_exp_date=cur_exp_date,
                period=1,
                return_xml=DEBUG
            )
            if DEBUG and isinstance(renew_result, tuple):
                result, xml = renew_result
                print("[Domain Demo] Renew result:", result)
                print("[Domain Demo] Renew response (XML):\n", xml)
            else:
                print(f"[Domain Demo] Renew result: {renew_result}")
        else:
            print("[Domain Demo] Could not find expiration date for renewal demo.")
        # --- DOMAIN TRANSFER DEMO ---
        print(f"[Domain Demo] Requesting transfer for domain: {test_domain}")
        # Use the original auth_info_pw from creation for transfer
        transfer_result = client.transfer_domain(
            domain_name=test_domain,
            auth_info="TestDomainAuth!123456",
            op="request",
            return_xml=DEBUG
        )
        if DEBUG and isinstance(transfer_result, tuple):
            result, xml = transfer_result
            print("[Domain Demo] Transfer result:", result)
            print("[Domain Demo] Transfer response (XML):\n", xml)
        else:
            print(f"[Domain Demo] Transfer result: {transfer_result}")
        # --- DOMAIN UPDATE DEMO ---
        print(f"[Domain Demo] Updating domain: {test_domain}")
        update_result = client.update_domain(
            domain_name=test_domain,
            add_ns=["ns3.example.net"],
            auth_info="NewDomainAuth!654321"
        )
        print(f"[Domain Demo] Update result: {update_result}")
        print(f"[Domain Demo] Deleting domain: {test_domain}")
        del_result = client.delete_domain(test_domain)
        print(f"[Domain Demo] Delete result: {del_result}")

        # --- DOMAIN RESTORE (RGP) DEMO ---
        print(f"[RGP Demo] Attempting to restore domain: {test_domain} (must be in redemption period)")
        restore_result = client.restore_domain_request(test_domain)
        print(f"[RGP Demo] Restore request result: {restore_result}")
        # Minimal restore: only domain name required
        print(f"[RGP Demo] Submitting restore report for domain: {test_domain} (minimal API)")
        report_result = client.restore_domain_minimal(test_domain)
        print(f"[RGP Demo] Restore report result: {report_result}")
    else:
        print(f"[Domain Demo] Domain creation failed, skipping info, renew, transfer, update and delete.")

    # --- DEMO: Hello command ---
    print("Sending <hello> to EPP server...")
    try:
        hello_result = client.hello(return_xml=DEBUG)
        if DEBUG and isinstance(hello_result, str):
            print("Hello response (XML):\n", hello_result)
        else:
            print("Hello parsed:", hello_result)
    except Exception as e:
        print(f"Error in hello: {e}")

    print("Logging in...")
    try:
        login_result = client.login(return_xml=DEBUG)
        if DEBUG and isinstance(login_result, tuple):
            success, xml = login_result
            print("Login success." if success else "Login failed.")
            print("Login response (XML):\n", xml)
        elif login_result:
            print("Login success.")
        else:
            print("Login failed.")
    except EPPConnectionLimitError as e:
        print(f"Connection error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    # --- DEMO: Contact create, info, delete, confirm deletion ---
    import random, string
    random_id = 'TEST-' + ''.join(random.choices(string.digits, k=6))
    print(f"\n[Contact Demo] Creating contact: {random_id}")
    contact_details = {
        'contact_id': random_id,
        'name': 'John Doe',
        'org': 'Example Inc.',
        'street': ['123 Example Dr.', 'Suite 100'],
        'city': 'Dulles',
        'pc': '20166-6503',
        'cc': 'US',
        'voice': '+1.7035555555',
        'email': 'jdoe@example.com',
        'auth_info_pw': '2fooBAR123456789!',
        'legal_form': 'CORP',
        'ident_value': '1234567890',
        'sp': 'VA',
        'fax': '+1.7035555556',
        'disclose': {'voice': None, 'email': None},
        'birth_date': None
    }
    create_result = client.create_contact(**contact_details)
    print("Create contact result:", create_result)

    print(f"[Contact Demo] Retrieving info for contact: {random_id}")
    info_result = client.info_contact(random_id)
    print("Contact info:", info_result)

    print(f"[Contact Demo] Deleting contact: {random_id}")
    delete_result = client.delete_contact(random_id)
    print("Delete contact result:", delete_result)

    print(f"[Contact Demo] Confirming deletion (should not exist): {random_id}")
    confirm_info = client.info_contact(random_id)
    print("Contact info after deletion:", confirm_info)

    # --- DEMO: Contact check ---
    print("\nChecking contact(s): TEST-0001, NEXT-0001")
    contact_check = client.check_contact(["TEST-0001", "NEXT-0001"])
    print("Contact check result:")
    for res in contact_check:
        print(f"  Contact: {res['id']}, Available: {res['available']}", end='')
        if 'reason' in res:
            print(f", Reason: {res['reason']}", end='')
        print()

    # --- DEMO: Host check ---
    print("\nChecking host(s): ns1.example.com, ns2.example.com")
    host_check = client.check_host(["ns1.example.com", "ns2.example.com"])
    print("Host check result:")
    for res in host_check:
        print(f"  Host: {res['name']}, Available: {res['available']}", end='')
        if 'reason' in res:
            print(f", Reason: {res['reason']}", end='')
        print()


    # --- DEMO: Check multiple domains ---
    domains_to_check = ["test.sk", "next.sk"]
    print(f"\nChecking domain(s): {', '.join(domains_to_check)}")
    check_result = client.check_domain(domains_to_check, return_xml=DEBUG)
    if DEBUG and isinstance(check_result, tuple):
        results, xml = check_result
        print("Check result:", results)
        print("Check response (XML):\n", xml)
    else:
        print("Check result:")
        for r in (check_result if isinstance(check_result, list) else [check_result]):
            print(f"  Domain: {r['domain']}, Available: {r['available']}")

    # --- DEMO: Info for a domain ---
    domain_info = "test.sk"
    print(f"\nGetting info for domain: {domain_info}")
    info_result = client.info_domain(domain_info, return_xml=DEBUG)
    if DEBUG and isinstance(info_result, tuple):
        result, xml = info_result
        print("Info result:", result)
        print("Info response (XML):\n", xml)
    else:
        print("Info result:")
        print(info_result)

    # --- DEMO: Info for a contact ---
    # Try to extract a real contact ID from last info_result, fallback to placeholder
    contact_id = None
    if isinstance(info_result, dict):
        contacts = info_result.get('contacts', {})
        # Use first contact ID from any contact type
        if contacts:
            for v in contacts.values():
                if v and isinstance(v, list):
                    contact_id = v[0]
                    break
    if not contact_id:
        contact_id = "sub_014524"  # fallback placeholder
    print(f"\nGetting info for contact: {contact_id}")
    contact_info = client.info_contact(contact_id, return_xml=DEBUG)
    if DEBUG and isinstance(contact_info, tuple):
        result, xml = contact_info
        print("Contact info result:", result)
        print("Contact info response (XML):\n", xml)
    else:
        print("Contact info result:")
        print(contact_info)

    # --- DEMO: Info for a non-existent host ---
    nonexist_host = 'ns1.sk-nic.sk'
    print(f"\nGetting info for non-existent host: {nonexist_host}")
    host_info = client.info_host(nonexist_host, return_xml=DEBUG)
    if DEBUG and isinstance(host_info, tuple):
        result, xml = host_info
        print("Host info result:", result)
        print("Host info response (XML):\n", xml)
        # Try to extract server message
        from lxml import etree
        try:
            root = etree.fromstring(xml.encode('utf-8'))
            msg_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}msg')
            if msg_elem is not None:
                print("Server message:", msg_elem.text)
        except Exception:
            pass
        if result.get('status') is None:
            print("[INFO] Host does not exist or no info available.")
    else:
        print("Host info result:")
        print(host_info)
        if isinstance(host_info, dict) and host_info.get('status') is None:
            print("[INFO] Host does not exist or no info available.")

    # --- HOST CREATE/UPDATE/DELETE DEMO ---
    import time
    host_suffix = int(time.time())
    test_host = f"ns-demo-{host_suffix}.example.net"
    ipv4 = "192.0.2.10"
    ipv6 = "2001:4860:4860::8888"
    print(f"\n[Host Demo] Creating host: {test_host}")
    create_result = client.create_host(
        host_name=test_host,
        addresses=[{'ip': ipv4, 'type': 'v4'}, {'ip': ipv6, 'type': 'v6'}],
        return_xml=DEBUG
    )
    if DEBUG and isinstance(create_result, tuple):
        result, xml = create_result
        print("[Host Demo] Create result:", result)
        print("[Host Demo] Create response (XML):\n", xml)
    else:
        print(f"[Host Demo] Create result: {create_result}")

    print(f"[Host Demo] Updating host: {test_host} (add IPv4, remove IPv6)")
    update_result = client.update_host(
        host_name=test_host,
        add_addrs=[{'ip': '198.51.100.5', 'type': 'v4'}],
        rem_addrs=[{'ip': ipv6, 'type': 'v6'}],
        return_xml=DEBUG
    )
    if DEBUG and isinstance(update_result, tuple):
        result, xml = update_result
        print("[Host Demo] Update result:", result)
        print("[Host Demo] Update response (XML):\n", xml)
    else:
        print(f"[Host Demo] Update result: {update_result}")

    print(f"[Host Demo] Deleting host: {test_host}")
    delete_result = client.delete_host(
        host_name=test_host,
        return_xml=DEBUG
    )
    if DEBUG and isinstance(delete_result, tuple):
        result, xml = delete_result
        print("[Host Demo] Delete result:", result)
        print("[Host Demo] Delete response (XML):\n", xml)
    else:
        print(f"[Host Demo] Delete result: {delete_result}")

    # --- DEMO: Info for an owned/existing host ---
    owned_host = os.environ.get('EPP_TEST_HOST', None)
    if owned_host and owned_host != nonexist_host:
        print(f"\nGetting info for your host: {owned_host}")
        host_info2 = client.info_host(owned_host, return_xml=DEBUG)
        if DEBUG and isinstance(host_info2, tuple):
            result, xml = host_info2
            print("Host info result:", result)
            print("Host info response (XML):\n", xml)
            from lxml import etree
            try:
                root = etree.fromstring(xml.encode('utf-8'))
                msg_elem = root.find('.//{urn:ietf:params:xml:ns:epp-1.0}msg')
                if msg_elem is not None:
                    print("Server message:", msg_elem.text)
            except Exception:
                pass
            if result.get('status') is None:
                print("[INFO] Host does not exist or no info available.")
        else:
            print("Host info result:")
            print(host_info2)
            if isinstance(host_info2, dict) and host_info2.get('status') is None:
                print("[INFO] Host does not exist or no info available.")
    else:
        print("[INFO] No owned host set in EPP_TEST_HOST, skipping owned host demo.")

    # --- DEMO: Check a random (likely non-existing) domain ---
    import random, string
    rand_domain = ''.join(random.choices(string.ascii_lowercase, k=10)) + ".sk"
    print(f"\nChecking random domain: {rand_domain}")
    rand_check = client.check_domain(rand_domain, return_xml=DEBUG)
    if DEBUG and isinstance(rand_check, tuple):
        results, xml = rand_check
        print("Random check result:", results)
        print("Random check response (XML):\n", xml)
    else:
        print("Random check result:")
        print(rand_check)

    # --- POLL DEMO ---
    print("\n[Poll Demo] Requesting next message in poll queue...")
    poll_result = client.poll_request(return_xml=DEBUG)
    if DEBUG and isinstance(poll_result, tuple):
        result, xml = poll_result
        print("[Poll Demo] Poll result:", result)
        print("[Poll Demo] Poll response (XML):\n", xml)
    else:
        print(f"[Poll Demo] Poll result: {poll_result}")
    msgQ = poll_result[0]['msgQ'] if (DEBUG and isinstance(poll_result, tuple)) else poll_result.get('msgQ')
    if msgQ and msgQ.get('id'):
        print(f"[Poll Demo] Acknowledging message ID: {msgQ['id']}")
        ack_result = client.poll_ack(msgQ['id'], return_xml=DEBUG)
        if DEBUG and isinstance(ack_result, tuple):
            result, xml = ack_result
            print("[Poll Demo] Ack result:", result)
            print("[Poll Demo] Ack response (XML):\n", xml)
        else:
            print(f"[Poll Demo] Ack result: {ack_result}")
    else:
        print("[Poll Demo] No message to acknowledge.")

    print("Logging out...")
    logout_response = client.logout()
    if DEBUG:
        print("Logout response (XML):\n", logout_response)
    else:
        print("Logged out.")

if __name__ == "__main__":
    main()

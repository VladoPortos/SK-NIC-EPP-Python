import secrets
import string

def generate_auth_info_pw(length=12):
    """
    Generate a secure SK-NIC compliant password for domain/contact auth_info_pw.
    Length: 8-16 chars. Includes upper, lower, digits, special chars.
    """
    if length < 8 or length > 16:
        length = 12
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    while True:
        pw = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Ensure at least one of each type
        if (any(c.islower() for c in pw)
            and any(c.isupper() for c in pw)
            and any(c.isdigit() for c in pw)
            and any(c in '!@#$%^&*' for c in pw)):
            return pw

from cyptography.fernet import Fernet
from django.conf import settings


fernet = Fernet(settings.MERAKI_API_SECRET_KEY.encode())

def encrypt_api_key(api_key: str) -> str:
    """Encrypts the given API key using Fernet symmetric encryption."""
    encrypted_key = fernet.encrypt(api_key.encode())
    return encrypted_key.decode()

def decrypt_api_key(encrypted_api_key: str) -> str:
    """Decrypts the given encrypted API key using Fernet symmetric encryption."""
    decrypted_key = fernet.decrypt(encrypted_api_key.encode())
    return decrypted_key.decode()
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    # genratingg a key using master password
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_password(password: str, master_password: str) -> str:
    key = generate_key(master_password)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password: str, master_password: str) -> str:
    key = generate_key(master_password)
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

# processor/encryptor.py

from Crypto.Cipher import AES
from base64 import b64encode
import os


def encrypt_log(log: str, key: str) -> str:
    """Encrypt log string using AES-256-GCM and return base64-encoded cipher."""
    key_bytes = key.encode()[:32].ljust(32, b'\0')
    nonce = os.urandom(12)
    cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(log.encode())
    return b64encode(nonce + tag + ciphertext).decode()

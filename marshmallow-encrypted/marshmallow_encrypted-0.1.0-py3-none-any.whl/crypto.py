from Crypto.Cipher import AES


def _to_bytes(value):
    return value.encode() if isinstance(value, str) else value


def encrypt(data, secret_key):
    cipher = AES.new(_to_bytes(secret_key), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, tag, cipher.nonce


def decrypt(ciphertext, tag, nonce, secret_key):
    cipher = AES.new(_to_bytes(secret_key), AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    cipher.verify(tag)
    return plaintext

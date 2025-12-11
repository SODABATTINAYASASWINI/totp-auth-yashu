import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key(path: str = "student_private.pem"):
    """Load RSA private key from PEM file."""
    with open(path, "rb") as f:
        pem_data = f.read()

    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,
    )
    return private_key


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP/SHA-256.

    Args:
        encrypted_seed_b64: Base64 string returned from instructor API
        private_key: RSA private key object

    Returns:
        64-character hex seed string
    """
    # 1. Base64 decode
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2. RSA OAEP decrypt (SHA-256)
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # 3. Decode bytes to string
    hex_seed = plaintext_bytes.decode("utf-8").strip()

    # 4. Validate: 64 hex characters
    if len(hex_seed) != 64:
        raise ValueError("Decrypted seed length is not 64 characters")

    allowed = set("0123456789abcdef")
    if not set(hex_seed.lower()) <= allowed:
        raise ValueError("Decrypted seed is not valid hex")

    return hex_seed

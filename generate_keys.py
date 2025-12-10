# generate_keys.py
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(key_size: int = 4096):
    # generate private key with public_exponent=65537
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )

    # private key PEM (unencrypted)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # PEM, compatible
        encryption_algorithm=serialization.NoEncryption()
    )

    # public key PEM (SubjectPublicKeyInfo)
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

if __name__ == "__main__":
    private_pem, public_pem = generate_rsa_keypair()
    # Write to files in the current working directory
    with open("student_private.pem", "wb") as f:
        f.write(private_pem)
    with open("student_public.pem", "wb") as f:
        f.write(public_pem)
    print("Keys generated successfully!")

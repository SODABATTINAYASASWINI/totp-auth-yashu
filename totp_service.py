import os
import base64
import binascii
import hashlib

import pyotp


def load_hex_seed(path: str = "data/seed.txt") -> str:
    """Load 64-character hex seed from file."""
    with open(path, "r", encoding="utf-8") as f:
        hex_seed = f.read().strip()
    if len(hex_seed) != 64:
        raise ValueError("Seed must be 64 hex characters")
    return hex_seed


def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex string to Base32 string (no padding).

    TOTP libraries expect Base32 secrets.
    """
    # hex -> bytes
    raw = binascii.unhexlify(hex_seed)
    # bytes -> base32
    b32 = base64.b32encode(raw).decode("utf-8")
    # Remove '=' padding (pyotp works fine without it)
    return b32.rstrip("=")


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code from hex seed.

    Config: SHA-1, 30s period, 6 digits (pyotp defaults).
    """
    secret_b32 = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(
        s=secret_b32,
        digits=6,
        interval=30,
        digest=hashlib.sha1,  # SHA-1
    )

    return totp.now()  # returns string like "123456"


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a 6-digit TOTP code with time window tolerance.

    valid_window = 1 means it accepts current, previous, next 30-second window.
    """
    secret_b32 = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(
        s=secret_b32,
        digits=6,
        interval=30,
        digest=hashlib.sha1,
    )

    # pyotp handles the time window logic
    return totp.verify(code, valid_window=valid_window)


if __name__ == "__main__":
    # Demo: generate and verify once
    hex_seed = load_hex_seed("data/seed.txt")

    code = generate_totp_code(hex_seed)
    print("Current TOTP code:", code)

    # Immediately verify the same code (should be True if run quickly)
    is_valid = verify_totp_code(hex_seed, code, valid_window=1)
    print("Verification result for that code:", is_valid)

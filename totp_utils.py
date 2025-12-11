import base64
import time
import hashlib
import pyotp


def _hex_to_base32(hex_seed: str) -> str:
    """Convert 64-char hex seed to Base32 string."""
    seed_bytes = bytes.fromhex(hex_seed)
    b32 = base64.b32encode(seed_bytes).decode("ascii")
    return b32


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code from 64-char hex seed.
    Config: SHA-1, 30s period, 6 digits.
    """
    b32_seed = _hex_to_base32(hex_seed)

    totp = pyotp.TOTP(
        b32_seed,
        digits=6,
        interval=30,
        digest=hashlib.sha1,
    )

    return totp.now()


def seconds_remaining(interval: int = 30) -> int:
    """Seconds left in current TOTP period."""
    now = int(time.time())
    return interval - (now % interval)


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a TOTP code with time window tolerance.

    valid_window=1 means accept codes from previous,
    current, and next 30s window.
    """
    b32_seed = _hex_to_base32(hex_seed)

    totp = pyotp.TOTP(
        b32_seed,
        digits=6,
        interval=30,
        digest=hashlib.sha1,
    )

    return totp.verify(code, valid_window=valid_window)


# optional small test
if __name__ == "__main__":
    with open("data/seed.txt", "r", encoding="utf-8") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    print("Current TOTP code:", code)
    print("Valid for ~", seconds_remaining(), "seconds")
    print("Verification result:", verify_totp_code(hex_seed, code))

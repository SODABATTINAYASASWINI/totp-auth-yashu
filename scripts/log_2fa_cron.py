#!/usr/bin/env python3

import os
from datetime import datetime, timezone
from totp_utils import generate_totp_code, seconds_remaining

SEED_FILE = "/data/seed.txt"

def read_hex_seed():
    if not os.path.exists(SEED_FILE):
        return None
    with open(SEED_FILE, "r") as f:
        return f.read().strip()

def main():
    hex_seed = read_hex_seed()
    if not hex_seed:
        print("No seed found")
        return

    code = generate_totp_code(hex_seed)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print(f"{now} - 2FA Code: {code}")

if __name__ == "__main__":
    main()

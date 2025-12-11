# #!/usr/bin/env python3

# import os
# from datetime import datetime, timezone
# from totp_utils import generate_totp_code, seconds_remaining

# SEED_FILE = "/data/seed.txt"

# def read_hex_seed():
#     if not os.path.exists(SEED_FILE):
#         return None
#     with open(SEED_FILE, "r") as f:
#         return f.read().strip()

# def main():
#     hex_seed = read_hex_seed()
#     if not hex_seed:
#         print("No seed found")
#         return

#     code = generate_totp_code(hex_seed)

#     now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

#     print(f"{now} - 2FA Code: {code}")

# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3

import base64
import pyotp
from datetime import datetime, timezone

# 1. Read seed
with open("/data/seed.txt", "r") as f:
    seed_hex = f.read().strip()

# Convert hex → base32
seed_bytes = bytes.fromhex(seed_hex)
seed_base32 = base64.b32encode(seed_bytes).decode()

# 2. Generate TOTP
totp = pyotp.TOTP(seed_base32)
code = totp.now()

# 3. Timestamp (UTC)
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

# 4. Print formatted output
print(f"{timestamp} - 2FA Code: {code}")

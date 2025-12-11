import os
from flask import Flask, request, jsonify

from crypto_utils import load_private_key, decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code, seconds_remaining

app = Flask(__name__)

SEED_FILE = "data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"


def read_hex_seed() -> str:
    if not os.path.exists(SEED_FILE):
        raise FileNotFoundError("Seed not decrypted yet")
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


# Endpoint 1: POST /decrypt-seed
@app.post("/decrypt-seed")
def decrypt_seed_endpoint():
    data = request.get_json(silent=True) or {}
    encrypted_seed_b64 = data.get("encrypted_seed")

    if not encrypted_seed_b64:
        return jsonify({"error": "Missing encrypted_seed"}), 400

    try:
        private_key = load_private_key(PRIVATE_KEY_FILE)
        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        with open(SEED_FILE, "w", encoding="utf-8") as f:
            f.write(hex_seed)

        return jsonify({"status": "ok"})
    except Exception as e:
        # in production you would not expose e, but for this task it is ok.
        return jsonify({"error": "Decryption failed", "details": str(e)}), 500


# Endpoint 2: GET /generate-2fa
@app.get("/generate-2fa")
def generate_2fa():
    try:
        hex_seed = read_hex_seed()
    except FileNotFoundError:
        return jsonify({"error": "Seed not decrypted yet"}), 500

    try:
        code = generate_totp_code(hex_seed)
        remaining = seconds_remaining()
        return jsonify({"code": code, "valid_for": remaining})
    except Exception as e:
        return jsonify({"error": "Failed to generate code", "details": str(e)}), 500


# Endpoint 3: POST /verify-2fa
@app.post("/verify-2fa")
def verify_2fa():
    data = request.get_json(silent=True) or {}
    code = data.get("code")

    if not code:
        return jsonify({"error": "Missing code"}), 400

    try:
        hex_seed = read_hex_seed()
    except FileNotFoundError:
        return jsonify({"error": "Seed not decrypted yet"}), 500

    try:
        ok = verify_totp_code(hex_seed, code, valid_window=1)
        return jsonify({"valid": ok})
    except Exception as e:
        return jsonify({"error": "Verification failed", "details": str(e)}), 500


if __name__ == "__main__":
    # Run local server on http://127.0.0.1:8000
    app.run(host="0.0.0.0", port=8000)

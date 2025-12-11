from crypto_utils import load_private_key, decrypt_seed

def main():
    # read encrypted seed that you already saved
    with open("encrypted_seed.txt", "r", encoding="utf-8") as f:
        encrypted_seed_b64 = f.read().strip()

    private_key = load_private_key("student_private.pem")
    hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

    print("Decrypted hex seed:", hex_seed)

    # store it as required by the task
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/seed.txt", "w", encoding="utf-8") as f:
        f.write(hex_seed)

    print("Saved hex seed to data/seed.txt")

if __name__ == "__main__":
    main()

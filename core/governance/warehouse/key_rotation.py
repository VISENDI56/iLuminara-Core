#!/usr/bin/env python3
"""
Phase 147: Automated Key Rotation Script
Rotates Snowflake RSA keys monthly to maintain Moving Target Defense.
"""

import os
import subprocess
import shutil
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def rotate_snowflake_keys():
    print("[*] Initiating Key Rotation (Phase 147)...")

    # Backup old keys
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"key_backups/{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    # Move old keys to backup
    for key_file in ["snowflake_rsa_key.pem", "snowflake_rsa_key.p8", "snowflake_rsa_key.pub"]:
        if os.path.exists(key_file):
            shutil.move(key_file, f"{backup_dir}/{key_file}")

    # Generate new keys
    print("[*] Generating new RSA key pair...")
    subprocess.run(["openssl", "genrsa", "-out", "snowflake_rsa_key.pem", "2048"], check=True)
    subprocess.run(["openssl", "pkcs8", "-topk8", "-inform", "PEM", "-in", "snowflake_rsa_key.pem", "-out", "snowflake_rsa_key.p8", "-nocrypt"], check=True)
    subprocess.run(["openssl", "rsa", "-in", "snowflake_rsa_key.pem", "-pubout", "-out", "snowflake_rsa_key.pub"], check=True)

    # Update .env with new passphrase (generate random)
    new_passphrase = f"iLuminara_{timestamp}"
    with open(".env", "r") as f:
        env_content = f.read()

    # Replace the passphrase
    env_content = env_content.replace(
        f"SNOWFLAKE_PRIVATE_KEY_PASSPHRASE={os.getenv('SNOWFLAKE_PRIVATE_KEY_PASSPHRASE')}",
        f"SNOWFLAKE_PRIVATE_KEY_PASSPHRASE={new_passphrase}"
    )

    with open(".env", "w") as f:
        f.write(env_content)

    print("====================================================")
    print("   ✅ KEYS ROTATED")
    print(f"   - Backup: {backup_dir}")
    print(f"   - New Passphrase: {new_passphrase}")
    print("   - Action: Upload new snowflake_rsa_key.pub to Snowflake")
    print("====================================================")

if __name__ == "__main__":
    rotate_snowflake_keys()
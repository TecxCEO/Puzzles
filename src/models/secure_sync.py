"""

To keep your medical or engineering logs private on GitHub, we will use AES-256 encryption via the cryptography library. This ensures that even if someone sees your files on GitHub, they cannot read the data without your unique password.
1. Install Encryption Library
In Termux, run:

pip install cryptography

2. Encryption & Sync Script (secure_sync.py)
This script encrypts your CSV file into a .dat file before pushing it to the cloud
"""
import os
from cryptography.fernet import Fernet
import subprocess

# 1. Setup Key (Run once and SAVE THIS KEY safely)
# key = Fernet.generate_key() 
# print(key.decode()) 
key = b'YOUR_SECRET_KEY_HERE' # Replace with your generated key
cipher = Fernet(key)

def encrypt_and_push():
    # Encrypt the file
    with open("expert_decisions_log.csv", "rb") as f:
        data = f.read()
    
    encrypted_data = cipher.encrypt(data)
    
    with open("encrypted_logs.dat", "wb") as f:
        f.write(encrypted_data)

    # Sync only the encrypted file to GitHub
    subprocess.run(["git", "add", "encrypted_logs.dat"])
    subprocess.run(["git", "commit", "-m", "Secure log sync"])
    subprocess.run(["git", "push", "origin", "main"])
    print("🔐 Encrypted logs pushed to GitHub!")

if __name__ == "__main__":
    encrypt_and_push()

"""
3. Safety Rules for Encryption
Never share your key: If you lose the key, you lose the data. Store it in a password manager.
Ignore the CSV: Add expert_decisions_log.csv to a .gitignore file so the raw, unencrypted data never accidentally gets uploaded.
Verification: To read your data back, you will need a small "Decryption" script on your PC using the same key.
Summary of your Expert Mobile Pipeline
Model: Sharded Weights (Puzzle 3) converted to TFLite.
Logic: Safety Monitor blocks dangerous actions.
UI: Kivy App for easy practitioner use.
Security: AES Encryption before syncing to GitHub via Wi-Fi.
"""

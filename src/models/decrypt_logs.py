"""

To view your encrypted logs on your PC, you need this decryption script. It reverses the AES encryption and restores the original CSV file so you can open it in Excel or Google Sheets.
1. The Decryption Script (decrypt_logs.py)
Run this on your computer (ensure you have pip install cryptography installed there too).
"""
from cryptography.fernet import Fernet
import os

# 1. Use the EXACT same key you used in Termux
# Replace this with your actual key string
key = b'3D5U6W21X0IhaTXnGbqUBsXFcLXRmtiLxRO0Kg4XJbY=' 
cipher = Fernet(key)

def decrypt_data():
    input_file = "encrypted_logs.dat"
    output_file = "decrypted_expert_logs.csv"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Download it from GitHub first.")
        return

    # Read the encrypted data
    with open(input_file, "rb") as f:
        encrypted_data = f.read()

    # Decrypt
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Save back to CSV
        with open(output_file, "wb") as f:
            f.write(decrypted_data)
        
        print(f"✅ Success! Your logs are now available in: {output_file}")
    except Exception as e:
        print(f"❌ Decryption failed. Check your key or file integrity. Error: {e}")

if __name__ == "__main__":
    decrypt_data()

"""

2. Workflow for Analysis
Sync from Phone: Run the secure_sync.py in Termux on your phone.
Download to PC: Use git pull on your PC to get the latest encrypted_logs.dat.
Decrypt: Run python decrypt_logs.py.
Review: Open decrypted_expert_logs.csv to see your model's performance and safety audits.
3. Critical Security Reminder
The Key is Everything: If you lose the key variable, the data in encrypted_logs.dat becomes permanently unreadable.
Local Use Only: Never commit your decrypt_logs.py to GitHub if it has the actual key written inside it.

"""

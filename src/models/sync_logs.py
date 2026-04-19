"""
To enable Cloud Sync for your expert system logs, you can use a Python script combined with Git to push updates to your GitHub repository. To ensure this only happens on Wi-Fi, we use the termux-api to check your connection status before running the sync.
1. Install Required Tools
In your Termux terminal, install the Git and API packages:

pkg install git termux-api
2. The Cloud Sync Script (sync_logs.py)
This script checks if you are connected to Wi-Fi. If yes, it commits your expert_decisions_log.csv and pushes it to GitHub.


"""

import subprocess
import json
import os

def is_on_wifi():
    try:
        # Check Wi-Fi status via Termux API
        result = subprocess.run(["termux-wifi-connectioninfo"], capture_output=True, text=True)
        data = json.loads(result.stdout)
        # If 'ip' exists and isn't 0.0.0.0, we are likely on Wi-Fi
        return data.get("ip") not in [None, "0.0.0.0"]
    except Exception:
        return False

def sync_to_github():
    if is_on_wifi():
        print("🌐 Wi-Fi detected. Syncing logs to GitHub...")
        commands = [
            ["git", "add", "expert_decisions_log.csv"],
            ["git", "commit", "-m", "Auto-sync expert logs"],
            ["git", "push", "origin", "main"]
        ]
        for cmd in commands:
            subprocess.run(cmd)
        print("✅ Sync complete.")
    else:
        print("🚫 No Wi-Fi. Sync postponed to save mobile data.")

if __name__ == "__main__":
    sync_to_github()
"""
3. Connect to your App
You can trigger this sync automatically in your main_app.py after every 10th decision, or simply add a "Sync Now" button to the UI that calls this script.
Why this is best for your Expert System:
Data Security: Your logs are backed up safely in the cloud in case your phone is lost or broken.
Cost Efficiency: By checking the connection, it avoids using your expensive mobile data for large log files.
Centralized Review: You can view the logs from your PC at any time by simply visiting your GitHub repository page. 
GitHub
GitHub
 +3
Pro-Tip: Automation
If you want this to run every hour in the background without opening the app, you can set up a Cron job in Termux: 
Gist
Gist
Run pkg install cronie.
Type crontab -e.
Add this line: 0 * * * * python ~/sync_logs.py (This runs the sync at the start of every hour).
"""

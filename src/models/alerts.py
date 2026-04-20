import subprocess

def send_thermal_alert(temp, status="PAUSE"):
    if status == "PAUSE":
        title = "❄️ Training Paused"
        msg = f"Phone reached {temp}°C. Cooling down for 5 mins..."
        sound = "default" # Plays your default notification sound
    else:
        title = "🚀 Training Resumed"
        msg = f"System cooled to {temp}°C. Re-starting batches."
        sound = "default"

    # Call Termux API
    subprocess.run([
        "termux-notification",
        "--title", title,
        "--content", msg,
        "--id", "thermal_monitor", # Overwrites previous notification
        "--priority", "high",
        "--led-color", "ff0000"
    ])


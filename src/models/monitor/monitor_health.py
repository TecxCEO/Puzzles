"""
To monitor your phone's health during this intensive task, we’ll create a System Health Monitor. This script tracks the Battery Drain, CPU Temperature, and RAM Usage while your training runs in the background.
1. Install Dependencies
You need the psutil library to access system hardware stats in Termux.

bash

pip install psutil

2. The Health Benchmark Script (monitor_health.py)


"""
import psutil
import time
import os

def get_temp():
    # Attempt to read the thermal sensor (path varies by phone)
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read()) / 1000
    except:
        return "N/A"

def monitor_system(duration_mins=10):
    print(f"--- 🔋 Starting 10-Minute Health Benchmark ---")
    start_time = time.time()
    end_time = start_time + (duration_mins * 60)
    
    initial_battery = psutil.sensors_battery().percent
    
    print(f"{'Time':<10} | {'Battery %':<10} | {'Temp °C':<8} | {'RAM %':<8}")
    print("-" * 45)

    while time.time() < end_time:
        battery = psutil.sensors_battery().percent
        temp = get_temp()
        ram = psutil.virtual_memory().percent
        elapsed = int(time.time() - start_time)
        
        print(f"{elapsed:>8}s | {battery:>9}% | {temp:>8} | {ram:>8}%")
        
        # Log to file for later analysis
        with open("health_log.csv", "a") as f:
            f.write(f"{elapsed},{battery},{temp},{ram}\n")
            
        time.sleep(30) # Sample every 30 seconds

    final_battery = psutil.sensors_battery().percent
    print("-" * 45)
    print(f"Benchmark Complete!")
    print(f"Total Battery Drop: {initial_battery - final_battery}%")

if __name__ == "__main__":
    monitor_system()

"""

"""

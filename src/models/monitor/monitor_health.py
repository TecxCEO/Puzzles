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
3. How to execute the "Stress Test"
Start Training: Launch your main_trainer.py in the background.
Start Monitor: Immediately run python monitor_health.py.
Wait: Let it run for 10 minutes.
4. What the Numbers Mean
Temp > 45°C: Your phone is "Thermal Throttling." It will slow down the CPU to stay cool, making your training take longer. Tip: Take off your phone case or place the phone on a cold surface.
RAM > 90%: You are close to a crash. Tip: Reduce the batch_size in your trainer.
Battery Drop > 5%: Training is very power-hungry. Tip: Keep the phone plugged into a charger (but watch the heat!).
5. Final Audit
Once finished, you can find the health_log.csv in your folder. You can move this to your Downloads to see the graphs:
bash
cp health_log.csv ~/storage/downloads/
"""

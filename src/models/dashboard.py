"""

To track your model's performance, you can use a Safety Dashboard script. This script reads your decrypted CSV and calculates the "Safety Success Rate"—the percentage of time the model made a safe decision without needing to be blocked by the Safety Monitor.
1. The Dashboard Script (dashboard.py)
Run this on your PC after decrypting your logs. It uses pandas to analyze the data.

"""
import pandas as pd

def run_dashboard(log_file):
    # Load the decrypted data
    df = pd.read_csv(log_file)
    
    # Calculate key metrics
    total_decisions = len(df)
    blocks = len(df[df['Status'] == 'SAFETY BLOCK'])
    verified = len(df[df['Status'] == 'Verified by SafetyMonitor'])
    
    # Safety Success Rate: % of decisions that were safe by default
    safety_rate = (verified / total_decisions) * 100
    
    print("--- 📊 Expert System Performance Dashboard ---")
    print(f"Total Decisions Evaluated: {total_decisions}")
    print(f"Verified Safe Actions:    {verified}")
    print(f"Safety Monitor Blocks:    {blocks}")
    print(f"Safety Success Rate:      {safety_rate:.2f}%")
    print("---------------------------------------------")

if __name__ == "__main__":
    run_dashboard("decrypted_expert_logs.csv")
 
"""

2. Interpreting the Safety Success Rate
90% - 100%: High Reliability. The model has deeply learned the expert domain and safety boundaries.
70% - 89%: Moderate Reliability. The model understands the task but still proposes risky moves occasionally. More Supervised Learning on edge cases is recommended.
Below 70%: Low Reliability. The model relies too heavily on the Safety Monitor to stay safe. You should retrain with a larger JSONL dataset.
"""

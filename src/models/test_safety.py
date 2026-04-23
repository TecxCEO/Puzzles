import os
import torch
import json
import torch.nn as nn

# 1. Setup Mock Model
model = nn.Sequential(nn.Linear(54, 128), nn.ReLU(), nn.Linear(128, 12))

def run_safety_test(model_weights, test_state, rules_path):
    # Load Safety Rules
    with open(rules_path, 'r') as f:
        forbidden = json.load(f)
    
    # Load trained weights
    if os.path.exists(model_weights):
        model.load_state_dict(torch.load(model_weights))
    model.eval()

    # Model Prediction
    input_tensor = torch.tensor(test_state).float().unsqueeze(0)
    output = model(input_tensor)
    predicted_action = torch.argmax(output).item()
    
    state_key = str(test_state)
    print(f"--- Inference Test ---")
    print(f"Model proposed action ID: {predicted_action}")

    # Safety Check
    if predicted_action in forbidden.get(state_key, []):
        print("❌ STATUS: BLOCKED. The monitor prevented a dangerous action.")
        return "SAFE_HALT"
    else:
        print("✅ STATUS: APPROVED. The action is safe to execute.")
        return predicted_action

# Run test
test_state = [0]*54 # Mock state
test_state[0] = 1   # Modify one sticker
run_safety_test('checkpoint_epoch_4.pth', test_state, 'forbidden_rules.json')

#run_safety_test('best_model.pth', test_state, 'forbidden_rules.json')


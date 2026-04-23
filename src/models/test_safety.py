#import encoder_decoder as ed
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
        return output, predicted_action
        #return predicted_action

# Run test
#test_state = [0]*54 # Mock state
# test_state[0] = 1   # Modify one sticker
#run_safety_test('best_model.pth', test_state, 'forbidden_rules.json')
####

# Encoder Decoder
import string


# here are all the unique characters that occur in this text
# Define the components
lowercase = string.ascii_lowercase          # a-z (26)
uppercase = string.ascii_uppercase          # A-Z (26)
digits = string.digits                      # 0-9 (10)
special = """ !.,{"'}()[]:;?-\n"""
# This works if you don't need a literal single quote in the middle
#special = ' !.,{"} ()[]:;?-\n' 
#special = " !.,{\"'}()[]:;?-\n"                     # Your 9 special chars (including space and newline)

# Combine them into one string
chars = lowercase + uppercase + digits + special
##chars = lowercase + uppercase + digits + special + ''.join(chars)
print(f"chars before sorted = {chars}")##
chars = sorted(list(set(chars)))
vocab_size = len(chars)
print(chars)
print(''.join(chars))
print(vocab_size)

# create a mapping from characters to integers
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string
#def encoder(input):
 # se = stoi[c] for c in s
####
if __name__ == "__main__":
    test_state = {
        "rgy":"ogw",
        "rgw":"ybo",
      "rby":"ryg",
      "rbw":"bwr",
      "ogy":"yrb",
      "ogw":"oyg",
      "oby":"owb",
      "obw":"wrg",
      "rb":"gy",
      "rg":"rw",
      "rw":"yr",
      "ry":"by",
      "ob":"gw",
      "og":"bw",
      "ow":"oy",
      "oy":"ow",
      "by":"go",
      "bw":"rb",
      "gw":"ob",
      "gy":"gr"
    }
    #test_state = ed.encode(test_state)
    test_state = encode(test_state)
    output, pa = run_safety_test('checkpoint_epoch_4.pth', test_state, 'forbidden_rules.json')
    #output = ed.decode(output)
    output = decode(output)
    print(f" Output = {output}")

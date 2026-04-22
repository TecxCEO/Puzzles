import json
import torch
import torch.nn as nn
from torch.utils.data import IterableDataset, DataLoader
import os

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

class ExpertDataset(IterableDataset):
    def __init__(self, file_path):
        self.file_path = file_path
    def __iter__(self):
        with open(self.file_path, 'r') as f:
            cube_data = json.load(f)
            #cube_data = json.read(f)
            cube=cube_data["solution"]
            cst, mv, amvst = get_nested_value(cube)
            cst = torch.tensor(encode(cst), dtype=torch.long)
            mv = torch.tensor(encode(mv), dtype=torch.long)
            amvst = torch.tensor(encode(afmvst), dtype=torch.long)
            yield torch.tensor(cst), torch.tensor(mv), torch.tensor(amvst)
            ####yield torch.tensor(data['state']), torch.tensor(data['move'])
            #for line in cube:
            #for key, line in cube.items():
                #data = json.loads(line)
                ###data = line
                ##data = torch.tensor(encode(text), dtype=torch.long)
                ##yield torch.tensor(data['state']), torch.tensor(data['move'])
                #yield torch.tensor(data['input']), torch.tensor(data['label'])
    
    def get_nested_value(data):
        """
        Recursively searches for a target_key in a nested dictionary.
        """
        mv=[]
        cst, amst={}
        # If the current element is a dictionary, look inside
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "state":
                    #yield value
                    cst=value
                elif len(key) == 3 and len(value)==20 :
                    #yield value
                    mv=key
                    amvst=value
                elif isinstance(value, dict) and len(value)==(16, 19) :
                    # If the value is another dictionary, dive deeper (recursion)
                    yield from get_nested_value(value)
                yield cst, mv, amvst
    
# 2. Safety Monitor def __init__(self, file_path):with Penalty Logic
class SafetyMonitor:
    def __init__(self, rules_path):
        with open(rules_path, 'r') as f:
            self.forbidden = json.load(f)
    def is_dangerous(self, state, action):
        state_key = str(state.tolist()) # Match JSON key format
        return action in self.forbidden.get(state_key, [])

# 3. Simple Model (Perfect for Termux/Mobile)
model = nn.Sequential(lm
    nn.Linear(54, 128),
    #nn.Linear(12, 128),
    nn.ReLU(),
    nn.Linear(128, 12) # 12 possible moves/actions
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()
monitor = SafetyMonitor('forbidden_rules.json')

# 4. The Training Loop
def start_training(epochs=5):
    dataset = ExpertDataset('cube3x3solvingdataset.json')
    #dataset = ExpertDataset('train_data.jsonl')
    loader = DataLoader(dataset, batch_size=16)
    
    for epoch in range(epochs):
        for batch_idx, (states, labels) in enumerate(loader):
            optimizer.zero_grad()
            outputs = model(states.float())
            predictions = torch.argmax(outputs, dim=1)
            
            # Apply Safety Penalty
            total_loss = 0
            for i in range(len(states)):
                if monitor.is_dangerous(states[i], predictions[i].item()):
                    # Create a high-penalty loss for this specific sample
                    loss = torch.tensor(10.0, requires_grad=True)
                else:
                    loss = criterion(outputs[i].unsqueeze(0), labels[i].unsqueeze(0))
                
                loss.backward(retain_graph=True)
                total_loss += loss.item()
            
            optimizer.step()
            if batch_idx % 20 == 0:
                print(f"Epoch {epoch} | Batch {batch_idx} | Avg Loss: {total_loss/16:.4f}")
        
        # Save progress
        torch.save(model.state_dict(), f"checkpoint_epoch_{epoch}.pth")

if __name__ == "__main__":
    start_training()


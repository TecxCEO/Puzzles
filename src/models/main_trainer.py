import json
import torch
import torch.nn as nn
from torch.utils.data import IterableDataset, DataLoader
import os

# 1. Memory-Efficient Data Streamer
class ExpertDataset(IterableDataset):
    def __init__(self, file_path):
        self.file_path = file_path
    def __iter__(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                yield torch.tensor(data['input']), torch.tensor(data['label'])

# 2. Safety Monitor with Penalty Logic
class SafetyMonitor:
    def __init__(self, rules_path):
        with open(rules_path, 'r') as f:
            self.forbidden = json.load(f)
    def is_dangerous(self, state, action):
        state_key = str(state.tolist()) # Match JSON key format
        return action in self.forbidden.get(state_key, [])

# 3. Simple Model (Perfect for Termux/Mobile)
model = nn.Sequential(
    nn.Linear(54, 128),
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


# Tecx Puzzle Solver Model


import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# 1. MODEL ARCHITECTURE
class PuzzleSolver(nn.Module):
    def __init__(self, input_dim=54, vocab_size=25, embed_dim=32):
        super().__init__()
        # Embedding handles the "tokens" (colors 0-5 and move IDs)
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(input_dim * embed_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 12) # 12 Possible moves
        )

    def forward(self, x):
        x = self.embedding(x)
        return self.network(x)

# 2. FLEXIBLE JSON DATASET
class NestedPuzzleDataset(Dataset):
    def __init__(self, json_file):
        self.samples = []
        with open(json_file, 'r') as f:
            data = json.load(f)
            for item in data:
                curr = item["current_state"]
                moves_data = item["next_move"]
                
                # Check if next_move is a list or single dict
                moves = moves_data if isinstance(moves_data, list) else [moves_data]
                for m in moves:
                    self.samples.append({
                        "input": torch.tensor(curr, dtype=torch.long),
                        "label": torch.tensor(m["action"], dtype=torch.long)
                    })

    def __len__(self): return len(self.samples)
    def __getitem__(self, idx): return self.samples[idx]["input"], self.samples[idx]["label"]

# 3. TRAINING FUNCTION
def train_model(data_path, epochs=10):
    dataset = NestedPuzzleDataset(data_path)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    model = PuzzleSolver()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for states, labels in loader:
            optimizer.zero_grad()
            outputs = model(states)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1} | Loss: {total_loss/len(loader):.4f}")
    
    return model

# 4. GENERATING RESULTS (INFERENCE)
def predict_next_move(model, current_state):
    model.eval()
    with torch.no_grad():
        state_tensor = torch.tensor([current_state], dtype=torch.long)
        output = model(state_tensor)
        move_id = torch.argmax(output, dim=1).item()
        return move_id

# --- EXECUTION ---
# Assuming 'data.json' follows your nested dictionary format
if __name__ == "__main__":
    # 1. Train
    # model = train_model('data.json')
    
    # 2. Predict/Generate Result
    sample_state = [0]*54 # Dummy state
    # move = predict_next_move(model, sample_state)
    # print(f"Predicted Move ID: {move}")
    print("Script ready. Adjust 'data.json' path to start.")

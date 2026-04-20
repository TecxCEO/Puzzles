"""
To prevent losing progress when training on a phone (where the app might close or the battery might die), you need to save the model weights and optimizer state to a .pth file.
Checkpoint-Enabled Training Script
This script saves your progress after every epoch and can automatically resume if it finds an existing checkpoint.
"""

import os
import torch

def save_checkpoint(model, optimizer, epoch, loss, filename="checkpoint.pth"):
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
    }
    torch.save(checkpoint, filename)
    print(f"--> Checkpoint saved: {filename}")

def load_checkpoint(model, optimizer, filename="checkpoint.pth"):
    if os.path.exists(filename):
        print(f"Loading checkpoint: {filename}")
        checkpoint = torch.load(filename)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return checkpoint['epoch'] + 1, checkpoint['loss']
    return 0, None # Start from scratch

# Integrated into your loop
def train_with_resume(jsonl_file, model, optimizer, criterion):
    start_epoch, _ = load_checkpoint(model, optimizer)
    
    for epoch in range(start_epoch, 10): # Training for 10 epochs
        # ... your training code here ...
        
        # At the end of every epoch, save progress
        save_checkpoint(model, optimizer, epoch, current_loss)


"""
Why this is critical for Termux

Resume after Crash: If Android's battery optimizer kills Termux, you can just run the script again and it will pick up exactly where it left off.
Transferability: You can move the checkpoint.pth to your Downloads folder, send it to a PC, and continue training there with more power.
Validation: You can use the checkpoint to "test" the model later without retraining everything.
How to see your saved weights
Once a checkpoint is saved, you can move it to your phone's main storage so it's safe:
bash
cp checkpoint.pth ~/storage/downloads/

"""

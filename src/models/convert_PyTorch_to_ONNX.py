import torch

# Load your trained model
from main_trainer import model 
#model.load_state_dict(torch.load('best_model.pth'))
model.load_state_dict(torch.load('checkpoint_epoch_4.pth'))
model.eval()

# Create dummy input (54 stickers)
dummy_input = torch.randn(1, 54)

# Export to ONNX
torch.onnx.export(model, dummy_input, "expert_model.onnx", 
                  input_names=['input'], output_names=['output'],
                  dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})

print("ONNX conversion complete: expert_model.onnx")


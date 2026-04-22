"""

#pip install onnxscript

If you run into "externally-managed-environment" errors:
Since you are using Python 3.13 in Termux, you might need to use a virtual environment or the --break-system-packages flag (use with caution) to install it:

#pip install onnxscript --break-system-packages
Why is this happening?
Newer versions of PyTorch (especially when running on newer Python versions like 3.13) have started utilizing onnxscript as the internal engine for ONNX exporting. Even if you didn't import it manually in your script, PyTorch's export function tries to import it behind the scenes.
Once installed, try running your script again:

#python convert_PyTorch_to_ONNX.py

"""
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


import string
import sys
import time
import datetime
import torch
from tecxlm import TecXModel
#from tecxlmtrain import TecXModel
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Define the exact 71 characters
#chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + " !.,:;?-\n"
##chars = "\n !,-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
#chars = "!,.:?CEFHILMTUWXYabcdefghiklmnopqrstuvwxy"
##chars = sorted(list(set(chars)))
##print(chars)
##print(len(chars))
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }

# Helper functions for the model
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])
##model_path = "tecxlm/TecXLM1.pth"
model_path = "tecxlm/tecxmodel.pth"
#model_path = "tecxlm/TecXLM.pth"
# model_path = Path("tecxlm") / "TecXLM.pth"
print(f"tecxmodelgen creating")
model = TecXModel()
##model = TecXModel(vocab_size=71)
###model.load_state_dict(torch.load(model_path))
checkpoint = torch.load(model_path)
model_dict = checkpoint["state_dict"]
chars = checkpoint["chars"]
##model_dict = model.state_dict()
# Filter out layers with wrong shapes (like lm_head)
####pretrained_dict = {k: v for k, v in checkpoint.items() if k in model_dict and v.size() == model_dict[k].size()}
#####model_dict.update(pretrained_dict)
model.load_state_dict(model_dict, strict=False)
#model.to(device)
# Ensure your model is in evaluation mode
model.eval()
print(f"tecxmodelgen created")
m = model.to(device)
m.eval()
"""
1. Set Up the Logger
Add this at the top of your tecxlmgenerate.py script. It creates a file named generation_logs.txt and appends new conversations to the bottom.

"""
def log_conversation(prompt, response):
    with open("generation_logs.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n{'='*50}\n")
        f.write(f"TIMESTAMP: {timestamp}\n")
        f.write(f"PROMPT: {prompt}\n")
        f.write(f"RESPONSE: {response}\n")
        f.write(f"{'='*50}\n")
        

"""
Update the Interactive Loop
Use sys.stdout.write and flush() to make the characters appear instantly on the same line.
"""
# ... inside your 'while True' loop ...
while True:
    # 1. Get custom text from the user
    #user_input = input("\nEnter your starting text (or type 'exit' to quit): ")
    user_prompt=input("\nEnter your starting text (or type 'exit' to quit): ")
    if user_prompt.lower() in ['exit', 'quit']:
        break
    length = input("How many tokens to generate? (default 100): ")
    num_tokens = int(length) if length.isdigit() else 100
    # Encode and setup context
    #context_list = [stoi[c] for c in user_prompt if c in stoi]
    #context = torch.tensor([context_list], dtype=torch.long, device=device)
    context = torch.tensor([encode(user_prompt)], dtype=torch.long).to(device)
    #data = torch.tensor(encode(user_prompt), dtype=torch.long)
    print(f"\n[TECX LM]: ", end="")
    sys.stdout.flush()
    # Set the creativity (temperature) and focus (top_k)
    temp = 0.4 # 1.0 is standard; higher is more creative, lower is more focused
    top_k = None # 5   # Keeps the model focused on the top 5 most likely characters
    tokens = 500 
    # max_new_tokens=num_tokens# Number of characters to generate
    with torch.no_grad():
        # Use the generator function
        # 1. Initialize an empty string to hold the output
        full_response = "" 
        # 2. Start the streaming loop
        #for token_id in model.generate_stream(context, tokens, temp, top_k):
        #for token_id in m.generate_stream(context, tokens, temp, top_k):
        for token_id in m.generate_stream(context, num_tokens, temp, top_k):
            ##char = decode(token_id)
            char = decode([token_id])
            sys.stdout.write(char)
            sys.stdout.flush()
            full_response += char # Collect for logging
            # Optional: Add a tiny sleep to make it look like "typing"
            time.sleep(0.01) 
    print("\n" + "-"*30)
    # Automatically save the conversation
    log_conversation(user_prompt, full_response)
    print("\n\n(Conversation saved to generation_logs.txt)")

"""
To make your model interactive, you can use Python’s input() function. This will pause the script and wait for you to type a "seed" (starting text) before the model begins generating.
Add this block to the bottom of your tecxlmgenerate.py script:
Interactive Generation Code

"""


# Ensure your model is in evaluation mode
#model.eval()

print("-" * 30)
print("TecX LLM Generation Mode")
print("-" * 30)

while True:
    # 1. Get custom text from the user
    user_input = input("\nEnter your starting text (or type 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        break

    # 2. Convert text to numbers using your encode function
    # Handle characters the model hasn't seen (OOD) to avoid crashes
    encoded_input = [stoi[c] for c in user_input if c in stoi]
    
    if not encoded_input:
        print("Error: None of those characters are in the model's vocabulary!")
        continue

    # 3. Create the input tensor [Batch Size, Time]
    # .unsqueeze(0) adds the batch dimension (size 1)
    context = torch.tensor(encoded_input, dtype=torch.long, device=device).unsqueeze(0)

    # 4. Generate and Decode
    print("\nGenerating...")
    # Adjust max_new_tokens for longer or shorter responses
    generated_indices = model.generate(context, max_new_tokens=200)[0].tolist()
    
    response = decode(generated_indices)
    #response = generated_indices
    print(f"\nModel Output:\n{response}")
    print("-" * 30)

"""
The Interactive Loop
This loop will ask for your text, handle the encoding, and call the function above.

"""
# Set the device (CPU or GPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

print("\n--- TecX LLM Interactive Session ---")

while True:
    prompt = input("\n[You]: ")
    if prompt.lower() in ['exit', 'quit']:
        break
        
    length = input("How many tokens to generate? (default 100): ")
    num_tokens = int(length) if length.isdigit() else 100

    # Encode prompt, ignoring characters not in training vocab
    context_indices = [stoi[c] for c in prompt if c in stoi]
    
    if not context_indices:
        print("Warning: None of those characters exist in my vocabulary. Starting with empty seed.")
        context = torch.zeros((1, 1), dtype=torch.long, device=device)
    else:
        context = torch.tensor([context_indices], dtype=torch.long, device=device)

    # Generate
    print("\n[Model]: ", end="")
    # We use [0] to extract the first batch and convert to list for decoding
    out_indices = model.generate(context, max_new_tokens=num_tokens)[0].tolist()
    print(decode(out_indices))
    

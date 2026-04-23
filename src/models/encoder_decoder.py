Encoder Decoder
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

import json
from puzzles.cubes.cube3x3.cube3x3 import CubeSolver as cs

class Solver():
  def __init__(self):
    csm=cs.moves()
    self.filename = "data.json"
    self.filepath="../data/cube3x3solution"
  def solve(self):
    
  def update_nested_key(self, data, target_key, new_value):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
        if target_key in data:
            data[target_key] = new_value
            return True
        for key, value in data.items():
            if update_nested_key(value, target_key, new_value):
                return True
                
    # If it's a list, check every item in the list
    elif isinstance(data, list):
        for item in data:
            if update_nested_key(item, target_key, new_value):
                return True
    
    return False
  def save_data_file(self):
    # --- HOW TO USE IT ---
    # 1. Load your file
    with open(filename, "r") as f:
      my_data = json.load(f)
    # 2. Update a key (no matter how deep it is) 
    # Example: Find "sms" and change it to True
    success = update_nested_key(my_data, "sms", True)
    if success:
      # 3. Save if the update happened
      with open(filename, "w") as f:
        json.dump(my_data, f, indent=4)
      print("Successfully updated the deep key!")
    else:
      print("Key not found in the file.")
if __name__=="__main__":
  state_given_to_solve={
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
  s=Solver()
  result=s.solve(state_given_to_solve)
  print(result)

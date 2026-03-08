import json
from puzzles.cubes.cube3x3.cube3x3 import CubeSolver as cs

class Solver():
  def __init__(self):
    csm=cs.moves()
    self.filename = "data.json"
    self.filepath="../data/cube3x3solution"
  def solve(self,given_state):
    self.current_state=given_state.copy()
    puzzle_data={
      "puzzle": {
        "Puzzle Given": self.current_state,
        "Puzzle Status":False,
        "Moves to Solve Puzzle":""
      },
      "solution":{}
    }
    with open(self.filename, "w") as f:
      #json.dump(puzzle_data, f, indent=4)
      json.dump(puzzle_data, f, indent=4)
    #update_nested_key(self, given_state)
    while True:
      # 1. Load your file
      with open(filename, "r") as f:
        my_data = json.load(f)
      # 2. Update a key (no matter how deep it is) 
      # Example: Find "sms" and change it to True
      success = update_nested_key(my_data[solution])
      #success = update_nested_key()
      if success[2]:
        # 3. Save if the update happened
        my_data[puzzle][Puzzle Status]=success[2]
        my_data[puzzle][Moves to Solve Puzzle]=success[1]
      with open(filename, "w") as f:
        json.dump(my_data, f, indent=4)
      print("Successfully updated the deep key!")
    #else:
     # print("Key not found in the file.")
  def update_nested_key(self,data,move=""):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
      #if target_key in data:
      if len(data)==20:
            #csm(data)
            return csm(data)
      elif len(data)==15 or len(data)==18:
        #elif len(data.items())==15 or len(data.items())==18:
        for key, value in data.items():
            if len(data)==15 or len(data)==18 or len(data)==20:
              #if len(data.items())==15 or len(data.items())==18 or len(data.items())==20:
              update_nested_key(value, key):
                return True
    return False
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

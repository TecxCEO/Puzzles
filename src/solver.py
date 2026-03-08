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
        "Puzzle_Given": self.current_state,
        "Puzzle_Status":False,
        "Moves_to_Solve_Puzzle":""
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
        my_data[puzzle][Puzzle_Status]=success[2]
        my_data[puzzle]["Moves_to_Solve_Puzzle"]=success[1]
        my_data[puzzle]["Puzzle_Solved_State"]=success[0]
      with open(filename, "w") as f:
        json.dump(my_data, f, indent=4)
      print("Successfully updated the deep key!")
    #else:
     # print("Key not found in the file.")
  def update_nested_key(self,data,move="",move_history=list()):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    moves_history=move_history
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
      #if target_key in data:
      if len(data)==20:
        states,moves,status=csm(data,move)
        if len(states)==15 or len(states)==18 and status is False:
          del data[:]
          for i in range(len(states)):
            data.[moves[i]]=states[i]
        elif len(states)==1 or len(moves)==1 and status is True:
          del data[:]
          for i in range(len(states)):
            data.[moves[i]]=states[i]
          return states, moves_history, status
        #csm(data)
        ##return csm(data,move)
      elif len(data)==15 or len(data)==18:
        #elif len(data.items())==15 or len(data.items())==18:
        for key, value in data.items():
            if len(data[key])==15 or len(data[key])==18 or len(data[key])==20:
              #if len(data.items())==15 or len(data.items())==18 or len(data.items())==20:
              moves_history.append(key)
              return update_nested_key(value, key,moves_history)
                #return True
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

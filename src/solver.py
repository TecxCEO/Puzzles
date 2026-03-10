import json
from cube3x3 import CubeSolver as cs
#import cube3x3
#from . import puzzles\cubes\cube3x3\cube3x3\CubeSolver as cs

class Solver(cs):
  def __init__(self):
    super().__init__()
    #self.c3s=CubeSolver
    #self.c3s=cs
    #self.c3cs=cs.CubeSolver
    self.filename = "data.json"
    self.filepath="../data/cube3x3/solution"
  def solve(self,given_state):
    self.current_state=given_state.copy()
    puzzle_data={
      "puzzle": {
        "Puzzle_Given": self.current_state,
        "Puzzle_Status":False,
        "Moves_to_Solve_Puzzle":""
      },
      "solution":self.current_state
      #"solution":self.current_state.copy()
    }
    with open(self.filename, "w") as f:
      json.dump(puzzle_data, f, indent=4)
    #update_nested_key(self, given_state)
    while True:
      while_loop=0
      print(f"whlieloop no = {(while_loop := while_loop + 1)} start.")
      l=31
      print(f"line no ={(l:=l+1)}")
      # 1. Load your file
      with open(self.filename, "r") as f:
        my_data = json.load(f)
      print(f"line no ={(l:=l+4)}")
      # 2. Update a key (no matter how deep it is) 
      # Example: Find "sms" and change it to True
      print(f"my data [solution]={my_data["solution"]}")
      print(f"line no ={(l:=l+4)}")
      result = self.update_nested_key(my_data["solution"])
      print(f"line no ={(l:=l+2)}")
      print(f"result={result}")
      success = list(result) if result is not None else [] 
      print(f"success={success}")
      print(f"line no ={(l:=l+1)}")
      if success and success[-1] is True:
        # 3. Save if the update happened
        my_data[puzzle][Puzzle_Status]=success[2]
        my_data[puzzle]["Moves_to_Solve_Puzzle"]=success[1]
        my_data[puzzle]["Puzzle_Solved_State"]=success[0]
        print(f"line no = 52")
        print(f"my data = {my_data}")
      with open(self.filename, "w") as f:
        json.dump(my_data, f, indent=4)
      print("Successfully updated the deep key!")
      print(f"whlieloop no = {while_loop} ends. and back to next one")
  def update_nested_key(self,data,move="",move_history=list()):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    rec_loop=0
    print(f"rec loop no = {(rec_loop:=  rec_loop+1)} start.")
    print(f"moves_history=move_history={moves_history}") if move_history else None
    rl=66
    moves_history=move_history
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
      #if target_key in data:
      if len(data)==20:
        rl=72
        print(f"line no ={rl}")
        states,move_list,status=super().moves(data,moves_history)
        #states,move_list,status=super().moves(data,move)
        #states,moves,status=cs.moves(data,move)
        if len(states) in [15,18] and len(move_list) in [15,18] and status is False:
          rl=77
          print(f"line no ={rl}")
          data.clear()
          print(f"data={data}")
          for i in range(len(states)):
            rl=83
            print(f"line no ={rl}")
            print(f"line no ={(rl:=81)}")
            data[move_list[i]]=states[i]
            print(f"data={data}")
        elif len(states)==1 or len(move_list)==1 and status is True:
          print(f"line no ={(rl:=85)}")
          data.clear()
          print(f"data={data}")
          for i in range(len(states)):
            print(f"line no ={(rl:=89)}")
            data[move_list[i]]=states[i]
            print(f"data={data}")
        return states, moves_history, status
      if len(data)==15 or len(data)==18:
        for key, value in data.items():
          print(f"line no ={(rl:=95)}")
          print(f"key={key} and value ={value}")
          if len(data[key])==15 or len(data[key])==18 or len(data[key])==20:
            print(f"line no ={(rl:=98)}")
            print(f"moves_history={moves_history}")
            if moves_history and moves_history[-1]!=key or moves_history=="":
              print(f"key={key} and value ={value} are selected")
              moves_history.append(key)
              print(f"line no ={(rl:=102)}")
              print(f"moves_history={moves_history}")
              return self.update_nested_key(value, key,moves_history)
    print(f"rec loop no = {rec_loop} end.")

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

import json
from cube3x3 import CubeSolver as cs

class Solver(cs):
  def __init__(self):
    super().__init__()
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
    }
    with open(self.filename, "w") as f:
      json.dump(puzzle_data, f, indent=4)
    while True:
      while_loop=0
      print(f"whlieloop no = {(while_loop := while_loop + 1)} start.")
      # 1. Load your file
      with open(self.filename, "r") as f:
        my_data = json.load(f)
      # 2. Update a key (no matter how deep it is) 
      # Example: Find "sms" and change it to True
      result = self.update_nested_key(my_data["solution"])
      success = list(result) if result is not None else []
      if success and success[-1] is True:
        # 3. Save if the update happened
        my_data[puzzle][Puzzle_Status]=success[2]
        my_data[puzzle]["Moves_to_Solve_Puzzle"]=success[1]
        my_data[puzzle]["Puzzle_Solved_State"]=success[0]
      with open(self.filename, "w") as f:
        json.dump(my_data, f, indent=4)
      print(f"whlieloop no = {while_loop} ends. and back to next one")
  def update_nested_key(self,data,moves_history=None):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    data_given=data ##
    d=data.copy() ##
    #data=data_given.copy()
    if moves_history is None:
      moves_history = []
    rec_loop=0
    print(f"rec loop no = {(rec_loop:=  rec_loop+1)} start.")
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
      if len(data)==20:
        if all(key and len(value) not in [15,18,20] for key, value in data.items()):
          print(f"line no ={83}")
          states,move_list,status=super().moves(data,moves_history)
          print(f"line no ={85}")
          print(f"moves_history={moves_history}")
          if len(states) in [15,18] and len(move_list) in [15,18] and status is False:
            for ml in moves_history:
              print(f"data given={data_given}")
              data_given=data_given[ml]
            data_given=[]
            print(f"data={data}")
            print(f"line of moves ={move_list}")
            print(f"status of puzzle solved ={status}")
            print(f"states after respective moves ={states}")
            for i in range(len(states)):
              data[move_list[i]]=[states[i]]
              print(f"data={data}")
          elif len(states)==1 or len(move_list)==1 and status is True:
            for ml in moves_history:
              print(f"data given={data_given}")
              data_given=data_given[ml]
            data_given=[]
            #data.clear()
            print(f"data={data}")
            for i in range(len(states)):
              print(f"line no ={(rl:=89)}")
              data[move_list[i]]=[states[i]]
              print(f"data={data}")
          return states, moves_history, status
        ##########№#####################################################
          # last change from here.
        ###elif all(key and len(value) in [15,18] for key, value in data.items()):
          ###print(f"line no ={(rl:=98)}")
          ###print(f"moves_history={moves_history}")
          ###moves_history.append(key)
          ###print(f"line no ={(rl:=101)}")
          ###print(f"moves_history={moves_history}")  
          ###return self.update_nested_key(value, key,moves_history)
      #if len(data)==15 or len(data)==18:
      #to here.
        ################################################### 
      if len(data)==15 or len(data)==18 or len(data)==20: 
        for key, value in data.items():
          print(f"line no ={(rl:=95)}")
          print(f"key={key} and value ={value}")
          if len(value) in [15,18,20] or len(data[key]) in [15,18,20]:
            print(f"line no ={(rl:=98)}")
            print(f"moves_history={moves_history}")
            if (moves_history and moves_history[-1]!=key) or not moves_history:
              print(f"key={key} and value ={value} are selected")
              print(f"moves_history={moves_history}")
              print(f"line no ={(rl:=102)}")
              print(f"moves_history={moves_history}")
              return self.update_nested_key(value,moves_history+[key])
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

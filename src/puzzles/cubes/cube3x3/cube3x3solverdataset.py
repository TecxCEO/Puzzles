import json
from cube3x3 import Cube3x3 as c3x3

class Solver(c3x3):
  def __init__(self):
    super().__init__()
    self.filename = "data.json"
    self.filepath="../data/cube3x3/solution"
  def solve(self,given_state):
    self.current_state=given_state.copy()
    puzzle_data={
      "puzzle": {
        "puzzle_given": self.current_state,
        "puzzle_status":False,
        "moves_to_solve_puzzle":""
      },
      "solution":self.current_state
    }
    with open(self.filename, "w") as f:
      json.dump(puzzle_data, f, indent=4)
    while_loop=0
    while True:
      print(f"whlieloop no = {(while_loop := while_loop + 1)} start.")
      # 1. Load your file
      with open(self.filename, "r") as rf:
        my_data = json.load(rf)
      # 2. Update a key (no matter how deep it is)      
      if my_data["puzzle"]["puzzle_status"]==False:
        self.update_nested_key(my_data["solution"],my_data["puzzle"]["puzzle_status"],my_data["puzzle"]["moves_to_solve_puzzle"])
        with open(self.filename, "w") as wf:
          json.dump(my_data, wf, indent=4)
      elif my_data["puzzle"]["puzzle_status"]==True:
        print( f"This Puzzle has been solved and The moves which were used to solve it, as followings")
        print(f"The moves for given puzzles solution ={my_data["puzzle"]["moves_to_solve_puzzle"]}")
        break
  def update_nested_key(self,data,status,mtsp,moves_history=None):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    print(f"moves_history={moves_history}")##
    if moves_history is None:
      moves_history = []
      status=False
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
      print(f"data length={len(data)}")
      if len(data)==20:
        print(f"so i am in if =20 condition")
        if all(key and len(value) not in [15,18,20] for key, value in data.items()):
          states,move_list,status=super().moves(data,mtsp,moves_history)
          print(f"moves_history={moves_history}")
          print(f"data={data}")####
          data.update({"state":data})
          print(f"data={data}")####
          #state_data=data
          #state_data=data.copy
          for dic_key in list(data.keys()):
            dic_value=data[dic_key]
            if not isinstance (dic_value,(dict,list)) and dic_key!=state:
              del data[dic_key]
          #if len(states) in [15,18] and len(move_list) in [15,18] and status is False:
          if len(states) in [1,15,18] and len(move_list) in [1,15,18]:
            print(f"data length= {len(data)}")
            for i in range(len(states)):
              data.update({move_list[i]:states[i]})
            #data.update({"state":state_data})#
            print(f"data={data}")####
          return data, moves_history, status 
      if len(data)==15 or len(data)==18 or len(data)==20:
        for key, value in data.items():
          print(f"key={key} and value ={value}")
          if len(value) in [15,18,20] or len(data[key]) in [15,18,20]:
            if (moves_history and moves_history[-1]!=key) or not moves_history:
              print(f"moves_history={moves_history}")
              self.update_nested_key(value,status,mtsp,moves_history+[key])
            if status == True and mtsp:
              print(f"mtsp={mtsp}")
              return
        return
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

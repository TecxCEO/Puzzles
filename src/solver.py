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
      with open(self.filename, "r") as rf:
        my_data = json.load(rf)
      # 2. Update a key (no matter how deep it is) 
      # Example: Find "sms" and change it to True
      ##print( f"my data before  unk function call={my_data}")
      ##result = self.update_nested_key(my_data["solution"])
      #states_option,moves,status = self.update_nested_key(my_data["solution"])
      self.update_nested_key(my_data["solution"])
      #success = list(result) if result is not None else []
      #if success and success[-1] is True:
      ####if status and status is True:
        # 3. Save if the update happened
        ###########my_data[puzzle][Puzzle_Status]=status
        ###############my_data[puzzle]["Moves_to_Solve_Puzzle"]=moves
        #my_data[puzzle]["Puzzle_Solved_State"]=states_option
        # 3. Save if the update happened
        #my_data[puzzle][Puzzle_Status]=success[2]
        #my_data[puzzle]["Moves_to_Solve_Puzzle"]=success[1]
        #my_data[puzzle]["Puzzle_Solved_State"]=success[0]
      #else:
      ##my_data.update({"solution":states_option})##
      print(f"my data={my_data}")
      with open(self.filename, "w") as wf:
        json.dump(my_data, wf, indent=4)
      ##print( f"my data after save to json file={my_data}")
      print(f"whlieloop no = {while_loop} ends. and back to next one")
  def update_nested_key(self,data,moves_history=None):
    """
    Searches recursively for 'target_key' and updates its value.
    Works for both nested dictionaries and lists of dictionaries.
    """
    print(f"moves_history={moves_history}")##
    if moves_history is None:
      moves_history = []
      ##states=[]
      ##move_list=[]
      status=False
    # If it's a dictionary, check keys or go deeper
    if isinstance(data, dict):
      print(f"data length={len(data)}")
      if len(data)==20:
        print(f"so i am in if =20 condition")
        if all(key and len(value) not in [15,18,20] for key, value in data.items()):
          states,move_list,status=super().moves(data,moves_history)
          print(f"moves_history={moves_history}")
          #cbe=[]
          #data_forward=data
          #for cb in data:
            #cbe=cbe+[cb]
            #print(f"data elements ={cbe}")
          #for cb in cbe:
            #del data_forward[cb]
          for dic_key in list(data.keys()):
            dic_value=data[dic_key]
            if not isinstance (dic_value,(dict,list)):
              del data[dic_key]
          #if len(states) in [15,18] and len(move_list) in [15,18] and status is False:
          if len(states) in [1,15,18] and len(move_list) in [1,15,18]:
            print(f"data length= {len(data)}")
            for i in range(len(states)):
              data.update({move_list[i]:states[i]})
              ##data[move_list[i]]=states[i]
              ####data_forward[move_list[i]]=states[i]
          ##elif len(states)==1 or len(move_list)==1 and status is True:
            ##for i in range(len(states)):
              ##data[move_list[i]]=[states[i]]
          ##return data_forward, moves_history, status
          return data, moves_history, status
          #return states, moves_history, status
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
          print(f"key={key} and value ={value}")
          if len(value) in [15,18,20] or len(data[key]) in [15,18,20]:
            if (moves_history and moves_history[-1]!=key) or not moves_history:
              print(f"moves_history={moves_history}")
              self.update_nested_key(value,moves_history+[key])
              #return self.update_nested_key(value,moves_history)
              ##data,moves_list,status=self.update_nested_key(value,moves_history+[key])
              #print(f"move key ={movekey}")
              #########if status is True:
                ##moves_history = move_list
                ##########return data,moves_history,status
        return
        #return data,moves_history,status
        ##return self.update_nested_key(value,moves_history+[key])
        #self.update_nested_key(value,moves_history+[key])
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

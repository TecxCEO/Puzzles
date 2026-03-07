import json

class CubeSolver:
  # move_paths={"rgy","rgw","rgo","rby","rbw","rbo","grw","gry","grb","gow","goy","gob","yrg","yrb","yrw","yog","yob","yow"}
  def __init__(self):
    self.output_file="./puzzle_move_and_states.json"
    faces={'b':'blue','g':'green','o':'orange','r':'red','y':'yellow','w':'white'}
    mutually_oppsite_side_faces={'blue':'green','orange':'red','yellow':'white'}
    self.mosf={'b':'g','g':'b','o':'r','r':'o','y':'w','w':'y'}
    colors={'blue','green','orange','red','yellow','white'}
    self.move_paths={"rgy","rgw","rgo","rby","rbw","rbo","grw","gry","grb","gow","goy","gob","yrg","yrb","yrw","yog","yob","yow"}
    vertex={
      "rgy":["red","green","yellow"],
      "rgw":["red","green","white"],
      "rby":["red","blue","yellow"],
      "rbw":["red","blue","white"],
      "ogy":["orange","green","yellow"],
      "ogw":["orange","green","white"],
      "oby":["orange","blue","yellow"],
      "obw":["orange","blue","white"]
    }
    edges={
      "rb":["red","blue"],
      "rg":["red","green"],
      "rw":["red","white"],
      "ry":["red","yellow"],
      "ob":["orange","blue"],
      "og":["orange","green"],
      "ow":["orange","white"],
      "oy":["orange","yellow"],
      "by":["blue","yellow"],
      "bw":["blue","white"],
      "gw":["green","white"],
      "gy":["green","yellow"]
    }
    # states={}
    self.solution={
      "rgy":"rgy",
      "rgw":"rgw",
      "rby":"rby",
      "rbw":"rbw",
      "ogy":"ogy",
      "ogw":"ogw",
      "oby":"oby",
      "obw":"obw",
      "rb":"rb",
      "rg":"rg",
      "rw":"rw",
      "ry":"ry",
      "ob":"ob",
      "og":"og",
      "ow":"ow",
      "oy":"oy",
      "by":"by",
      "bw":"bw",
      "gw":"gw",
      "gy":"gy"
    }
    state_given={
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
  #def next_moves(last_move):
   # moves={}
    #for m in range(18):
     # if(last_move.strip()[:2]!=move_paths[m].strip()[:2]):
      #  moves[m]=move_paths[m]
    #return moves
  def mover(self,moving_step,state):
    print(f"move={moving_step}")
    f=moving_step.strip()[0]
    print(f"f={f}")
    s=moving_step.strip()[1]
    print(f"s={s}")
    cc=moving_step.strip()[2]
    print(f"cc={cc}")
    if f!= self.mosf[cc]and f!=cc:
      c=moving_step.strip()[2]
    elif f == self.mosf[cc]and f!=cc:
      for mosf in self.mosf:
        if mosf != f and mosf != s and mosf != self.mosf[f] and mosf != self.mosf[s]:
          c=mosf
          break
    print(f"c={c}")
    moving_block=[]
    mb={}
    moving_block.append(f"{f}{s}{c}")
    moving_block.append(f"{f}{s}{self.mosf[c]}")
    moving_block.append(f"{self.mosf[f]}{s}{c}")
    moving_block.append(f"{self.mosf[f]}{s}{self.mosf[c]}")
    moving_block.append(f"{f}{s}")
    moving_block.append(f"{s}{c}")
    moving_block.append(f"{self.mosf[f]}{s}")
    moving_block.append(f"{s}{self.mosf[c]}")
    print(f"State Elements = {state}")
    print(f"Moving Blocks = {moving_block}")
    for name in moving_block:
      print(f"Moving Block = {name}")
      st_e=""
      for state_element in state:
        if sorted(name) == sorted(state_element):
          print(f"Given State {state_element} element has value= {state[state_element]} /n This valule will be saved to Moving block {name} element after this {moving_step} move ")
          for n in range(len(name)):
            for se in range(len(state_element)):
              if state_element.strip()[se]==name.strip()[n]:
                st_e+=state[state_element].strip()[se]
      if st_e!="":
        mb.update({name:st_e})
    print(f"Elements of moving block={mb}")
    mbc=mb
    if self.mosf[f]!=cc:
      # #
      a=mb[f"{f}{s}{c}"] #
      print(f"Before mb{f}{s}{c}={a}") # #
      ac=mbc[f"{f}{s}{self.mosf[c]}"] #
      print(f"Before mbc{f}{s}{self.mosf[c]}={ac}") # #
      # #
      mb[f"{f}{s}{c}"]=mbc[f"{f}{s}{self.mosf[c]}"]
      # #
      a=mb[f"{f}{s}{c}"] #
      print(f"After mb{f}{s}{c}={a}") #
      a=mb[f"{s}{c}"] #
      print(f"Before mb {s}{c} ={a}") #
      ac= mbc[f"{f}{s}"]#
      print(f"Before mbc {f}{s} ={ac}") #
      # #
      mb[f"{s}{c}"]=mbc[f"{f}{s}"]
      # #
      a=mb[f"{s}{c}"] #
      print(f"After ={a}") #
      a= mb[f"{self.mosf[f]}{s}{c}"] #
      print(f"Before mb {self.mosf[f]}{s}{c} ={a}") #
      ac=mbc[f"{f}{s}{c}"] #
      print(f"Before mbc {f}{s}{c} ={ac}") #
      # #
      mb[f"{self.mosf[f]}{s}{c}"]=mbc[f"{f}{s}{c}"]
      # #
      a=mb[f"{self.mosf[f]}{s}{c}"] #
      print(f"After mb {self.mosf[f]}{s}{c} ={a}") #
      a= mb[f"{self.mosf[f]}{s}"] #
      print(f"Before mb {self.mosf[f]}{s}={a}") #
      ac=mbc[f"{s}{c}"] #
      print(f"Before mbc {s}{c} ={ac}") #
      # #
      mb[f"{self.mosf[f]}{s}"]=mbc[f"{s}{c}"]
      # #
      a= mb[f"{self.mosf[f]}{s}"] #
      print(f"After mb {self.mosf[f]}{s}={a}") #
      a=mb[f"{self.mosf[f]}{s}{self.mosf[c]}"] #
      print(f"Before mb {self.mosf[f]}{s}{self.mosf[c]}  ={a}") #
      ac= mbc[f"{self.mosf[f]}{s}{c}"] #
      print(f"Before mbc {self.mosf[f]}{s}{c}    ={ac}") #
      # #
      mb[f"{self.mosf[f]}{s}{self.mosf[c]}"]=mbc[f"{self.mosf[f]}{s}{c}"]
      # #
      a= mb[f"{self.mosf[f]}{s}{self.mosf[c]}"] #
      print(f"After mb {self.mosf[f]}{s}{self.mosf[c]} ={a}") #
      a= mb[f"{s}{self.mosf[c]}"] #
      print(f"Before mb {s}{self.mosf[c]} = {a}") #
      ac= mbc[f"{self.mosf[f]}{s}"] #
      print(f"Before mbc {self.mosf[f]}{s}   ={ac}") #
      # #
      mb[f"{s}{self.mosf[c]}"]=mbc[f"{self.mosf[f]}{s}"]
      # #
      a= mb[f"{s}{self.mosf[c]}"]  #
      print(f"After mb {s}{self.mosf[c]}  ={a}") #
      a= mb[f"{f}{s}{self.mosf[c]}"] #
      print(f"Before  mb {f}{s}{self.mosf[c]} =  {a}") #
      ac= mbc[f"{self.mosf[f]}{s}{self.mosf[c]}"] #
      print(f"Before mbc {self.mosf[f]}{s}{self.mosf[c]} ={ac}") #
      # #
      mb[f"{f}{s}{self.mosf[c]}"]=mbc[f"{self.mosf[f]}{s}{self.mosf[c]}"]
      # #
      a= mb[f"{f}{s}{self.mosf[c]}"]   #
      print(f"After  mb {f}{s}{self.mosf[c]}   ={a}") #
      a=  mb[f"{f}{s}"] #
      print(f"Before  mb {f}{s}   ={a}") #
      ac= mbc[f"{s}{self.mosf[c]}"] #
      print(f"Before  mbc {s}{self.mosf[c]}   ={ac}") #
      # #
      mb[f"{f}{s}"]=mbc[f"{s}{self.mosf[c]}"]
      # #
      a=mb[f"{f}{s}"] #
      print(f"After mb {f}{s}   ={a}") #
      # #
    elif self.mosf[f]==cc:
      # #
      a= mb[f"{self.mosf[f]}{s}{c}"]#
      print(f"Before  mb {self.mosf[f]}{s}{c}  ={a}") #
      ac=mbc[f"{f}{s}{self.mosf[c]}"] #
      print(f"Before  mbc {f}{s}{self.mosf[c]} ={ac}") #
      # #
      mb[f"{self.mosf[f]}{s}{c}"]=mbc[f"{f}{s}{self.mosf[c]}"]
      # #
      a= mb[f"{self.mosf[f]}{s}{c}"]  #
      print(f"After mb {self.mosf[f]}{s}{c}   ={a}") #
      a= mb[f"{self.mosf[f]}{s}"]  #
      print(f"Before mb {self.mosf[f]}{s}  ={a}") #
      ac=mbc[f"{f}{s}"] #
      print(f"Before  mbc {f}{s} ={ac}") #
      # #
      mb[f"{self.mosf[f]}{s}"]=mbc[f"{f}{s}"]
      # #
      a= mb[f"{self.mosf[f]}{s}"]#
      print(f"After  mb {self.mosf[f]}{s}  ={a}") #
      a=mb[f"{self.mosf[f]}{s}{self.mosf[c]}"] #
      print(f"Before mb {self.mosf[f]}{s}{self.mosf[c]}  ={a}") #
      ac=mbc[f"{f}{s}{c}"] #
      print(f"Before mbc {f}{s}{c}  ={ac}") #
      # #
      mb[f"{self.mosf[f]}{s}{self.mosf[c]}"]=mbc[f"{f}{s}{c}"]
      # #
      a= mb[f"{self.mosf[f]}{s}{self.mosf[c]}"] #
      print(f"After  mb {self.mosf[f]}{s}{self.mosf[c]} ={a}") #
      a=mb[f"{s}{self.mosf[c]}"] #
      print(f"Before mb {s}{self.mosf[c]}  ={a}") #
      ac=mbc[f"{s}{c}"] #
      print(f"Before mbc {s}{c} ={ac}") #
      # #
      mb[f"{s}{self.mosf[c]}"]=mbc[f"{s}{c}"]
      # #
      a= mb[f"{s}{self.mosf[c]}"] #
      print(f"After mb {s}{self.mosf[c]} ={a}") #
      a= mb[f"{f}{s}{self.mosf[c]}"]#
      print(f"Before mb {[f]}{s}{self.mosf[c]}  ={a}") #
      ac=mbc[f"{self.mosf[f]}{s}{c}"] #
      print(f"Before  mbc {self.mosf[f]}{s}{c} ={ac}") #
      # #
      mb[f"{f}{s}{self.mosf[c]}"]=mbc[f"{self.mosf[f]}{s}{c}"]
      # #
      a= mb[f"{f}{s}{self.mosf[c]}"] #
      print(f"After  mb {[f]}{s}{self.mosf[c]}  ={a}") #
      a= mb[f"{f}{s}"]#
      print(f"Before mb {f}{s} ={a}") #
      ac=mbc[f"{self.mosf[f]}{s}"] #
      print(f"Before mbc {self.mosf[f]}{s}   ={ac}") #
      # #
      mb[f"{f}{s}"]=mbc[f"{self.mosf[f]}{s}"]
      # #
      a=mb[f"{f}{s}"] #
      print(f"After mb {f}{s} ={a}") #
      a= mb[f"{f}{s}{c}"] #
      print(f"Before mb {f}{s}{c}={a}") #
      ac=mbc[f"{self.mosf[f]}{s}{self.mosf[c]}"] #
      print(f"Before  mbc {self.mosf[f]}{s}{self.mosf[c]}  ={ac}") #
      # #
      mb[f"{f}{s}{c}"]=mbc[f"{self.mosf[f]}{s}{self.mosf[c]}"]
      # #
      a= mb[f"{f}{s}{c}"] #
      print(f"After mb {f}{s}{c}   ={a}") #
      a=mb[f"{s}{c}"] #
      print(f"Before mb {s}{c}   ={a}") #
      ac= mbc[f"{s}{self.mosf[c]}"]#
      print(f"Before mbc {s}{self.mosf[c]}   ={ac}") #
      # #
      mb[f"{s}{c}"]=mbc[f"{s}{self.mosf[c]}"]
      # #
      a= mb[f"{s}{c}"] #
      print(f"After  mb {s}{c} ={a}") #
      # #
    print(f"After move the elements of moving block={mb}")
    for name in moving_block:
      mb_e=""
      for state_element in state:
        if sorted(name) == sorted(state_element):
          print(f"Moving block {name} element has value = {mb[name]} /n this value will be save to Given State {state_element} element after this {moving_step} move")
          for se in range(len(state_element)):
            for n in range(len(name)):
              if state_element.strip()[se]==name.strip()[n]:
                mb_e+=mb[name].strip()[n]
      if mb_e!="":
        state.update({state_element:mb_e})
    print(f"Current state of puzzle after this {moving_step} move state={state}")
    return state
    
  ##def moves(self, state, move_history="", move_list=move_paths ):
  def moves(self, state, move_history="" ):
    # moves_to=list(move_list)
    moves_to=list(self.move_paths)
    cur_state=state
    i=0
    states = {}
    puzzle_solve= False
    last_move=""
    move_path_history=list(move_history)
    while cur_state!=self.solution and i<len(moves_to):
      if move_path_history!="" and move_path_history:
        last_move=move_path_history[-1] # if move_path_history else None
        print(f"Last Move = {move_path_history[-1]}")
        while True:
          if last_move.strip()[:2]!=moves_to[i].strip()[:2]:
            print(f"last_move strip [:] = {last_move.strip()[:]}")
            print(f"last_move strip [:2] = {last_move.strip()[:2]}")
            break
          elif last_move.strip()[:2]==moves_to[i].strip()[:2]:
            i+=1
            print(f"i = i")
      states[i] = self.mover(moves_to[i],cur_state)
      move_path_history.append(moves_to[i])
      # Prepare the JSONL entry
      data_entry = {
        "given state":"",
        "current state":states[i],
        "move": moves_to[i],
        "moved_steps_list":move_path_history,
        "metadata": {
          "source": "Fuzzle Solver",
          "length": len(move_path_history)
        }
        }
      # Append to the JSONL file
      with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data_entry) + '\n')
      print(f"Successfully Saved")
      # last_move=moves_to[i]
      # next_moves_list=[]
      # next_moves_list=next_moves(last_move)
      ##for to_move in moves_to:
        ##if last_move.strip()[:2]!=to_move.strip()[:2]:
          ##print(f"last_move strip [:] = {last_move.strip()[:]}")
          ##print(f"last_move strip [:2] = {last_move.strip()[:2]}")
          ##print(f"to_move strip [:2] = {to_move.strip()[:]}")
          ##print(f"to_move strip [:2] = {to_move.strip()[:2]}")
          ##next_moves_list.append(to_move)
        # states[i], move_path_history, puzzle_solve = self.moves(states[i], next_moves_list, move_path_history)
      if states[i]==self.solution:
        print(f"This fuzzle have been solved.")
        print(f"This fuzzle have been solved. ###################################################################################################################################################################################")
        puzzle_solve=True
        return states[i], move_path_history, puzzle_solve
      return self.moves(states[i], move_path_history) ##
      ## return self.moves(states[i], next_moves_list, move_path_history) ##
      i=i+1
if __name__=="__main__":
  state_given={
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
  cs=CubeSolver()
  result=cs.moves(state_given)
  print(result)

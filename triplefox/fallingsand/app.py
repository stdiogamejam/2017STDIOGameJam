#!/usr/bin/python3

"""Falling Sand Game, August 20, 2017. 
MIT license, see LICENSE for details."""

"""Display a choice list, take & validate user input,
then return the name and index of the user's choice."""
def input_choice(choicear):
  while True:
    choicedisplay = []
    for cidx in range(len(choicear)):
      if cidx < len(choicear):
        choicedisplay.append(str(cidx + 1)+") "+choicear[cidx])
    print("  ".join(choicedisplay))
    print("Please enter a number:")
    try:
      usercommit = int(input(">"))
      if usercommit >= 1 and usercommit <= len(choicear):
        return (choicear[usercommit - 1], usercommit - 1)
    except:
      pass
    print("Please enter a number between 1 and "+str(len(choicear)))

"""Take, validate, and return user input for an integer number."""
def input_int(msg, minv, maxv):
  while True:
    print(msg, "("+str(minv)+" - "+str(maxv)+")")
    try:
      usercommit = int(input(">"))
      if usercommit >= minv and usercommit <= maxv:
        return usercommit
    except:
      pass

"""Render the grid of particles and optionally a cycle count
or cursor for the editor."""
def render(grid, render_table, cycle, cursor_x, cursor_y):
  result = ""
  for y in range(grid["h"]):
    widx = grid["w"]*y
    for x in range(grid["w"]):
      if cursor_x == x and cursor_y == y:
        result += "@"
      else:
        result += render_table[grid["d"][widx + x]]
    result += "\n"
  print(result)
  if cycle > 0:
    print("Cycle #"+str(cycle))

"""Convenience functions for working with the grid data."""

def make_grid(w,h):
  return {"w":w,"h":h,"d":[0 for n in range(w*h)]}
def copy_grid(src):
  return {"w":src["w"],"h":src["h"],"d":[n for n in src["d"]]}
def set_grid(grid, x, y, v):
  if x >= 0 and x < grid["w"] and y >= 0 and y < grid["h"]:
    grid["d"][grid["w"] * y + x] = v
def get_grid(grid, x, y):
  if x >= 0 and x < grid["w"] and y >= 0 and y < grid["h"]:
    return grid["d"][grid["w"] * y + x]
  else:
    return 0
def set_rect_grid(grid, x, y, w, h, v):
  for x0 in range(w):
    for y0 in range(h):
      set_grid(grid, x + x0, y + y0, v)

"""Constants for the particles."""
AIR, SAND, WATER, FIRE, OIL, STONE = 0, 1, 2, 3, 4, 5
"""Characters used to display the particles."""
render_table = [".",";","~","*","O","#"]

"""Which (relative) positions the particles check. Multiple tables
are used to produce behaviors that depend on the cycle count."""
sand_fall_table = [(0,1),(-1,1),(1,1),(0,0)]
fire_rise_table_0 = [(0,-1),(1,1)]
fire_rise_table_1 = [(0,-1),(-1,-1)]
water_fall_table_0 = [(0,1),(-1,1),(-1,0)]
water_fall_table_1 = [(0,1),(1,1),(1,0)]

"""In each collision scenario of (source, destination), mutate to
the given result values."""
sand_collide_table = []
sand_collide_table.append(((SAND,AIR),(AIR,SAND)))
sand_collide_table.append(((SAND,WATER),(WATER,SAND)))
sand_collide_table.append(((SAND,FIRE),(AIR,SAND)))
water_collide_table = []
water_collide_table.append(((WATER,AIR),(AIR,WATER)))
water_collide_table.append(((WATER,FIRE),(AIR,AIR)))
water_collide_table.append(((WATER,OIL),(OIL,WATER)))
fire_collide_table = []
fire_collide_table.append(((FIRE,AIR),(AIR,FIRE)))
fire_collide_table.append(((FIRE,SAND),(AIR,SAND)))
fire_collide_table.append(((FIRE,OIL),(FIRE,FIRE)))
fire_collide_table.append(((FIRE,STONE),(AIR,STONE)))
oil_collide_table = []
oil_collide_table.append(((OIL,AIR),(AIR,OIL)))
oil_collide_table.append(((OIL,FIRE),(FIRE,FIRE)))
oil_collide_table.append(((FIRE,SAND),(AIR,SAND)))

"""Associate each particle constant with rules for falling and collision."""
tablespace = [
  (SAND,(sand_fall_table,),sand_collide_table),
  (WATER,(water_fall_table_0,water_fall_table_1),water_collide_table),
  (OIL,(water_fall_table_0,water_fall_table_1),oil_collide_table),
  (FIRE,(fire_rise_table_0,fire_rise_table_1),fire_collide_table)
]

"""Update the entire grid."""
def grid_update(g0, cycle):
  g1 = copy_grid(g0) # each cycle writes to a new grid
  for particle_type, particle_fall, particle_collide in tablespace:
    # iterate over the whole grid looking for this particle type:
    for y0 in range(g0["h"]):
      for x0 in range(g0["w"]):
        if get_grid(g0, x0, y0) == particle_type:
        # decide which falling rules to use based on current cycle,
          for p in particle_fall[cycle % len(particle_fall)]:
            # if the rule succeeded in producing a result, we're done
            if particle_update(x0, y0, p, g0, g1, particle_collide):
              break
  return g1

"""Update a single particle in a single fall configuration."""
def particle_update(x0, y0, p, g0, g1, particle_collide):
  x1, y1 = p[0] + x0, p[1] + y0 # destination position
  v0, v1 = get_grid(g0, x0, y0), get_grid(g0, x1, y1)
  # try to match a scenario to the two positions and their contents
  for collide_scenario, collide_result in particle_collide:
    if v0 == collide_scenario[0] and v1 == collide_scenario[1]:
      set_grid(g1, x0, y0, collide_result[0])
      set_grid(g1, x1, y1, collide_result[1])
      return True
  return False

"""Run the simulation some number of times."""
def run_simulation(grid, times, cycle):
  for n in range(times):
    cycle = cycle + 1
    grid = grid_update(grid, cycle)
    render(grid, render_table, cycle, -1, -1)
  return cycle

"""State machine to run editing display and commands."""
class Editor(object):
  def __init__(self):
    self.state = "Options"
    self.x = 0
    self.y = 0
  def fsm(self, grid):
    arrowchoices = ["Left <-","Down v","Up ^","Right ->"]
    particlechoices = ["Air","Sand","Water","Oil","Fire","Stone"]
    if self.state == "Options":
      render(grid, render_table, -1, self.x, self.y)
      choices = arrowchoices + particlechoices + ["Bye"]
      self.state, idx = input_choice(choices)
    elif self.state in arrowchoices:
      if self.state == "Left <-":
        self.x -= 1
      elif self.state == "Right ->":
        self.x += 1
      elif self.state == "Up ^":
        self.y -= 1
      elif self.state == "Down v":
        self.y += 1
      self.wrap_cursor(grid)
      self.state = "Options"
    elif self.state in particlechoices:
      if self.state == "Air":
        set_grid(grid, self.x, self.y, AIR)
      elif self.state == "Sand":
        set_grid(grid, self.x, self.y, SAND)
      elif self.state == "Water":
        set_grid(grid, self.x, self.y, WATER)
      elif self.state == "Fire":
        set_grid(grid, self.x, self.y, FIRE)
      elif self.state == "Oil":
        set_grid(grid, self.x, self.y, OIL)
      elif self.state == "Stone":
        set_grid(grid, self.x, self.y, STONE)
      print("Set "+str((self.x,self.y))+" to "+self.state)
      self.state = "Options"
    else:
      raise "Invalid state "+self.state
  def wrap_cursor(self, grid):
    if self.x < 0:
      self.x += grid["w"]
    if self.y < 0:
      self.y += grid["h"]
    self.x = self.x % grid["w"]
    self.y = self.y % grid["h"]

"""State machine to run game modes, the grid and cycle count."""
class Persist(object):
  def __init__(self):
    self.state = "Intro"
    gw, gh = 10, 10
    self.grid = make_grid(gw,gh)
    self.cycle = 0
    set_rect_grid(self.grid, 0, 0, 4, 2, SAND)
    set_rect_grid(self.grid, 0, gh-1, gw, 1, STONE)
    set_rect_grid(self.grid, gw-3, 0, 3, 2, WATER)
    set_rect_grid(self.grid, gw-2, 3, 2, 2, OIL)
    set_rect_grid(self.grid, gw-2, gh-2, 2, 2, FIRE)
  def fsm(self):
    if self.state == "Intro":
      print("              Welcome to the Falling Sand Game!")
      print("  By James Hofmann (Triplefox). Made during \"stdio jam\", 2017")
      print("---------------------------------------------------------------")
      print("In this game, particles of sand, water, and other elements are ")
      print("simulated on a grid. Each time the simulation advances a cycle,")
      print("the sand falls one square, colliding with any nearby particles.")
      print("")
      print(". - Air: Passes other particles")
      print("# - Stone: Blocks other particles")
      print("; - Sand: Falls, blocks other particles")
      print("* - Fire: Rises, dies when blocked")
      print("~ - Water: Falls, douses fire")
      print("O - Oil: Falls, lit up by fire")
      print("")
      print("")
      self.state = "Options"
    elif self.state == "New":
      print("Setting up a new grid.")
      gw = input_int("Please enter a grid width in columns:", 0, 80)
      gh = input_int("Please enter a grid height in rows:", 0, 20)
      self.grid = make_grid(gw,gh)
      self.state = "Options"
    elif self.state == "Run":
      run_count = input_int("Enter number of cycles to run:", 0, 1000)
      run_simulation(self.grid, run_count, self.cycle)
      self.state = "Options"
    elif self.state == "Edit":
      editor = Editor()
      while editor.state != "Bye":
        editor.fsm(self.grid)
      self.state = "Options"
    elif self.state == "Options":
      self.state, idx = input_choice(["New","Run","Edit","Bye"])
    else:
      raise "Invalid state: "+self.state

persist = Persist()
while persist.state != "Bye":
  persist.fsm()
print("Thanks for playing!")

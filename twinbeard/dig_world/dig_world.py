from math import cos, sin
from random import random, randint
import pickle
import re

# Empty class to store data
class DataStore(): pass

# Where all the game data is stored
game = DataStore()

def main():
  # Initialize game
  game.live_boulders = []    # Locations of boulders that are about to fall
  game.world_size    = 12    # How big the current world is
  game.move_queue    = ""    # Moves the miner has entered, yet to be executed
  game.bank_money    = 0     # How much money the miner has in the bank
  game.carried_money = 0     # How much money the miner is carrying
  game.light         = 2     # How much of the world is displayed at once
  game.max_ladders   = 5     # How many ladders the miner can carry
  game.ladders       = 5     # How many ladders the miner is carrying
  game.parachute     = True  # Whether the miner has a parachute
  game.helmet        = True  # Whether the miner has a helmet
  game.dead          = False # Whether the miner is dead
  
  generateWorld()    
  
  print("Welcome to Dig World, the world of digging!")

  while not game.dead:
    determineAvailableMoves()
    requestMoves()
    makeMove()
    settleBoulders()

  print("\nYour adventure ends here! Final score: $"+str(game.bank_money))

def generateWorld():
  game.world = []
  
  # Randomized world parameters
  xs = (random()*0.1+0.4) * (random()<0.5 and 1 or -1)
  xo, yo = random()*50, random()*50

  # Generate world and put stuff in it
  for y in range(game.world_size):
    row = []
    for x in range(game.world_size): 
      # This weirdo function generates caves at roughly the scale we want
      if sin((x*xs+y/2)-xo)+cos((y/2+sin(x*xs)*20)-yo)>0.8: row.append(".")
      elif random() < 0.7:  row.append("\"") # Add dirt 
      elif random() < 0.6:  row.append("0")  # Add a boulder
      elif random() < 0.02: row.append("n")  # Add a chest
      else: row.append("$")                  # Add treasure
    game.world.append(row)
  
  # Put the miner at the top middle of the map  
  game.miner_pos = Vec2(int(game.world_size/2), -1)
  
  # If that's not on top of solid ground, try random spots until one is
  while not solidAt(game.miner_pos.add(Vec2(0, 1))):
    game.miner_pos = Vec2(randint(0, game.world_size-1), -1)
    
  # Place a single gate near the bottom of the map
  setTile(Vec2(randint(0, game.world_size-1), \
               randint(game.world_size-6, game.world_size-1)), "%")

# The following functions, determineAvailableMoves, requestMoves, makeMove and
# settleBoulders, comprise the main game loop
               
def displayGameState():
  # Display surrounding environment
  s = "\n"
  for y in range(game.miner_pos.y-game.light, game.miner_pos.y+game.light+1):
    if y < -1 or y > game.world_size: continue
    if y < 0 and game.miner_pos.y >= 0: continue
    for x in range(game.miner_pos.x-game.light, game.miner_pos.x+game.light+1):
      if x < -1 or x>game.world_size: continue
      if game.miner_pos.eq(Vec2(x, y)): s += "@"
      else: s += tileAt(Vec2(x, y))
    s += "\n"
  print(s)

  # Display HUD
  print("Bank: $%d Carried treasure: $%d Ladders: %d Depth: %d\'%s%s" % \
    (game.bank_money, game.carried_money, game.ladders, game.miner_pos.y*10+10,
     game.parachute and " Parachute" or "", game.helmet and " Helmet" or ""))
  
  # Display available commands. The string "udlrgqos" specifies the order the
  # commands are shown in.
  print(" ".join(["%s) %s"%(k.upper(), game.cmds[k][0]) \
                    for k in "udlrgqos" if k in game.cmds]))
  
  # If at surface, display available shop items. The string "bcph" specifies
  # the order the items are shown in.
  if atSurface():
    print("\nShop:")
    for k in "bcph":
      if k in game.cmds: print(" ", game.cmds[k][0].title())

def determineAvailableMoves():
  # Always available commands
  game.cmds = \
  { 
    "u": ("Go up", doGo), "d": ("Go down", doGo), "l": ("Go left", doGo),
    "r": ("Go right", doGo), "q": ("Quit", doQuit), "o": ("Load", doLoad)
  }
  
  # If on top of a gate, can enter the gate
  if tileAt(game.miner_pos)=="%": game.cmds["g"] = ("Enter gate", doGate)
  
  # If at surface, can save and use the shop
  if atSurface(): 
    game.cmds["s"] = ("Save", doSave)
    for item in shopItems(): game.cmds[item[0]] = ("%s) $%d %s"%item[:3], doBuy)
    
# Get commands from player, if none are queued up
def requestMoves():
  while game.move_queue=="":
    displayGameState()
    game.move_queue = input("\nEnter command or list of commands: ")
    
    # Replace sequences like 10u with uuuuuuuuuu, so the player doesn't have
    # to type u a bunch of times in a row
    game.move_queue = re.sub(r"(\d+)([a-z])", \
      lambda m: m.group(2)*int(m.group(1)), game.move_queue)
    
    print

# Execute player's next command in the queue, if valid
def makeMove():    
  move = game.move_queue[0].lower()
  game.move_queue = game.move_queue[1:]
  
  if move in game.cmds: game.cmds[move][1](move)
  else: print("Ignoring unknown/unavailable command:", move)

  # After each move, make the player fall, if appropriate
  if tileAt(game.miner_pos)=="H": return
  
  distance = 0
  
  while not solidAt(game.miner_pos.add(Vec2(0, 1))):
    game.miner_pos.y += 1
    distance += 1
    
  # Determine outcome of falling
  if distance > 3:
    if game.parachute:      
      print("You fall", distance*10, \
        "feet. Luckily, your parachute opens and you land safely!")
      game.parachute = False
    else:
      print("You fall", distance*10, "feet, to your death!")
      game.dead = True
  elif distance > 0:
    print("You fall", distance*10, "feet!")

def settleBoulders():
  # Items that will be removed from boulder list, since we can't remove items
  # from an array while it's being iterated over
  goners = []
  
  for boulder in game.live_boulders:
    # Tick down until the boulder is ready to fall
    if boulder[1] > 0:
      boulder[1]-=1
      continue

    # Prepare to remove from live boulder list
    goners.append(boulder)
    
    setTile(boulder[0], ".")
    
    # Fall until stopped, trashing ladders and miners along the way!
    destroyed_ladders = 0    
    while not solidAt(boulder[0].add(Vec2(0, 1)), "H@"):
      boulder[0].y += 1
      
      if tileAt(boulder[0])=="H":
        setTile(boulder[0], ".")
        destroyed_ladders += 1
      
      if game.miner_pos.eq(boulder[0]):
        if game.helmet:
          print("The falling boulder destroys your helmet!")
          game.helmet = False
        else:
          print("The falling boulder kills you!")
          game.dead = True
          return
      
    setTile(boulder[0], "0")
    if destroyed_ladders > 0:
      print("The falling boulder lands after destroying", destroyed_ladders, \
            "ladder" + (destroyed_ladders!=1 and "s" or "") + ".")
    else: print("The falling boulder lands.")
  
  # Actually remove settled boulders from array
  for boulder in goners: game.live_boulders.remove(boulder)  

# The following functions, starting with "do," are commands the miner might
# execute.

def doQuit(move): game.dead = input("Are you sure? (Y/N) ").lower()=="y"

def doSave(move):
  with open(input("Filename? "), "wb") as f: pickle.dump(game, f)
  print("\nSaved!")
  
def doLoad(move):
  global game
  try:
    with open(input("Filename? "), "rb") as f: game = pickle.load(f)
    print("\nWelcome back!")
  except:
    print("\nLoad failed!")

def doBuy(move):
  for item in shopItems():
    if item[0]==move:
      if game.bank_money < item[1]: print("You can't afford it!")
      else:
        game.bank_money -= item[1]
        item[3](item[1])

# Enter gate and spawn a new, larger world
def doGate(move):
  game.world_size = int(game.world_size*3/2+5)
  generateWorld()
  reachSurface(True)
  
def doGo(move):
  if move=="u": dir = Vec2( 0, -1)
  if move=="d": dir = Vec2( 0,  1)
  if move=="l": dir = Vec2(-1,  0)
  if move=="r": dir = Vec2( 1,  0)
    
  new_pos = game.miner_pos.add(dir)

  current_tile = tileAt(game.miner_pos)
  new_tile     = tileAt(new_pos)
  
  # If climbing, try to use a ladder
  if dir.y < 0 and current_tile!="H":
    if game.ladders == 0:
      print("You can't go up because you don't have any ladders!")
      return
    if atSurface():
      print("You can't go up because you're already on the surface!")
      return
    if current_tile=="%":
      print("You can't place a ladder over the gate!")
      return
    game.ladders -= 1
    setTile(game.miner_pos, "H")
    print("You drop a ladder to climb.")
    
  # Don't move into impassable objects    
  for b in [("0=", "into boulders"), ("|-", "past the edge of the world")]:
    if new_tile in b[0]:
      print("You can't dig %s!"%b[1])
      return

  # Interact with stuff in the world
  if solidAt(new_pos, "H%"):  
    # Loose treasure
    if new_tile == "$":
      print("You found some treasure, worth $"+str(int(new_pos.y/5+1))+"!")
      game.carried_money += int(new_pos.y/5+1)
    # Treasure chest
    elif new_tile == "n":
      if random() < 0.5:
        print("You find $%d of treasure in the chest!" % (game.world_size*2))
        game.carried_money += game.world_size*2
      elif random() < 0.25 and not game.helmet:
        print("You find a helmet in the chest!")
        game.helmet = True
      elif random() < 0.25 and not game.parachute:
        print("You find a parachute in the chest!")
        game.parachute = True
      elif random() < 0.5:
        print("You find a ladder upgrade in the chest!")
        game.max_ladders += 1
        game.ladders = game.max_ladders
      else:
        print("You find a lamp upgrade in the chest!")
        game.light += 1
    # Dirt
    elif dir.x==-1: print("You dig left.")
    elif dir.x== 1: print("You dig right.")
    elif dir.y==-1: print("You dig up.")
    elif dir.y== 1: print("You dig down.")
    
    # No matter what the item is, it goes away now
    setTile(new_pos, ".")
  
  # Returning to surface with this move?
  if not atSurface() and new_pos.y==-1: reachSurface(False)
  
  # Actually perform the move
  game.miner_pos = new_pos
  
  if new_tile=="%": print("You found a gate to another world!")
  
  # Unsettle any boulders above the miner.
  boulders_released = 0
  above = game.miner_pos.add(Vec2(0, -1))
 
  # Adding from bottom to top is important, because boulders will fall in the
  # order added to the list.
  while tileAt(above)=="0":
    setTile(above, "=")
    boulders_released += 1
    game.live_boulders.append([above.clone(), 1])
    above.y -= 1
    
  if   boulders_released >  1: print("The boulders above begin to shake!")
  elif boulders_released == 1: print("The boulder above begins to shake!")

# Determine available shop options
def shopItems():
  # Functions to actually execute the purchase of the specified item.
  def buyLadder(price):
    game.max_ladders += 1
    game.ladders = game.max_ladders
    print("Ladder capacity increased!")
      
  def buyLamp(price):
    game.light += 1
    print("Lamp brightness increased!")
    
  def buyParachute(price):
    game.parachute = True
    print("You buy the parachute!")
      
  def buyHelmet(price):
    game.helmet = True
    print("You buy the helmet!")
      
  # Build a data structure of available items in the shop
  s = [("b", 2**(game.light-1),       "Upgrade lamp brightness", buyLamp), \
       ("c", 2**(game.max_ladders-4), "Upgrade ladder capacity", buyLadder)]
  if not game.parachute: s.append(("p", 100, "Buy parachute", buyParachute))
  if not game.helmet:    s.append(("h", 100, "Buy helmet",    buyHelmet))
  
  return s

def reachSurface(new_world):
  if new_world: print("You emerge from the gate into a larger world!")
  else: print("Welcome back to the surface! You can use the shop again.")
  
  if game.carried_money>0: 
    print("You deposit $"+str(game.carried_money)+" in the bank.")
  game.bank_money += game.carried_money
  game.carried_money = 0    
  
  print("You refill your ladders.")
  game.ladders = game.max_ladders
  
def atSurface(): return game.miner_pos.y==-1

# Return whether a given location is solid -- space, dot, and the characters
# specified in the ignore string are considered to be empty.
def solidAt(pos, ignore=""): return tileAt(pos) not in ignore+" ."

def setTile(pos, tile): game.world[pos.x][pos.y] = tile

# Look up tile at location in the world, with special cases for the edge of
# the world.
def tileAt(p):  
  if p.y==game.world_size: return "-"
  if p.x==-1 or p.x==game.world_size: return "|"
  if p.x<-1 or p.x>game.world_size or p.y<0 or p.y>game.world_size: return " "
  return game.world[p.x][p.y]

# Barebones 2D Vector class; only the methods we need.
class Vec2:
  def __init__(_, x, y): _.x, _.y = x, y    
  def eq (_, v): return _.x==v.x and _.y==v.y
  def add(_, v): return Vec2(_.x+v.x, _.y+v.y)
  def clone(_): return Vec2(_.x, _.y)
  
# Python idiom to call main() if this module is being executed directly
if __name__=="__main__": main()

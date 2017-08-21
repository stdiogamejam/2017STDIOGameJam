# Changes from Dig World:
# - Replaced explit saves with checkpointing when you're at the surface.
# - Designed levels rather than randomized, with story scenes before and after.
# - Removed parachute and helmet.
# - Changed the % from a gate to a relic. You need to return to the surface
#   to advance to the next level.
# - Added arrow and spike traps that activate after you pick up the relic.

import copy
import json
from math import cos, sin
from random import random, randint
import re
import textwrap

# Empty class to store data
class DataStore(): pass

# Where all the game data is stored
game = DataStore()

def main():
  # Initialize game
  game.live_boulders = []    # Locations of boulders that are about to fall
  game.move_queue    = ""    # Moves the miner has entered, yet to be executed
  game.bank_money    = 0     # How much money the miner has in the bank
  game.carried_money = 0     # How much money the miner is carrying
  game.light         = 3     # How much of the world is displayed at once
  game.max_ladders   = 5     # How many ladders the miner can carry
  game.ladders       = 5     # How many ladders the miner is carrying
  game.relic         = False # Whether the miner has the relic
  game.realm         = None  # The realm the miner is on
  game.current_realm = 0     # The realm number the miner is on
  game.checkpoint    = None  # Game state to be restored when the player dies
  game.quit          = False # Whether the player has quit
  
  print("Welcome to Dig World Realms!")

  nextRealm()
  
  while not game.quit:
    if atSurface(): saveCheckpoint()
    determineAvailableMoves()    
    requestMoves()
    makeMove()
    settleBoulders()

def saveCheckpoint():
  # Don't save the upcoming move sequence with the checkpoint
  saved_moves = game.move_queue
  game.queued_moves = ""
  
  # Clear out the existing checkpoint so it doesn't get saved inside the new one
  game.checkpoint = None
  game.checkpoint = copy.deepcopy(game)
  
  game.move_queue = saved_moves
    
def restoreCheckpoint():
  print(textwrap.fill("You shake out of your reverie, still at the surface. " +
                      "That won't work out -- gotta think of something else!"))
  global game
  game = copy.deepcopy(game.checkpoint)
  
def nextRealm():
  with open("realms.json") as f: realms = json.load(f)
  
  game.realm = realms[game.current_realm]  

  # Have to do rotate the level design data because of the dumb way it's
  # oriented!
  game.world = []  
  game.world_size = Vec2(len(game.realm["world"][0]), len(game.realm["world"]))
  for x in range(game.world_size.x):
    s = []
    for y in range(game.world_size.y):
      s.append(game.realm["world"][y][x].replace("#", "\""))
    game.world.append(s)    

  print("\n"+textwrap.fill(game.realm["intro"]))
 
  # Use next realm, wrap around if we've reached the end
  game.current_realm = (game.current_realm+1)%len(realms)
  
  # Put the miner at the top of the map
  game.miner_pos = Vec2(int(game.world_size.x/2), -1)
     
# The following functions, determineAvailableMoves, requestMoves, makeMove and
# settleBoulders, comprise the main game loop

# Display game state
def showWorld():
  s = "\n"
  for y in range(game.miner_pos.y-game.light, game.miner_pos.y+game.light+1):
    if y < -1 or y > game.world_size.y: continue
    if y < 0 and game.miner_pos.y >= 0: continue
    for x in range(game.miner_pos.x-game.light, game.miner_pos.x+game.light+1):
      if x < -1 or x>game.world_size.x: continue
      if game.miner_pos.eq(Vec2(x, y)): s += "@"
      else: s += tileAt(Vec2(x, y))
    s += "\n"
  print(s)

  # Display HUD
  print("Bank: $%d Carried treasure: $%d Ladders: %d Depth: %d\'" % \
    (game.bank_money, game.carried_money, game.ladders, game.miner_pos.y*10+10))

def displayGameState():
  showWorld()  
  
  # Display available commands. The string "udlrgqe" specifies the order the
  # commands are shown in.
  print(" ".join(["%s) %s"%(k.upper(), game.cmds[k][0]) \
                    for k in "udlrges" if k in game.cmds]))
  
  # If at surface, display available shop items. The string "bc" specifies
  # the order the items are shown in.
  if atSurface():
    print("\nShop:")
    for k in "bc":
      if k in game.cmds: print(" ", game.cmds[k][0].title())

def determineAvailableMoves():
  # Always available commands
  game.cmds = \
  { 
    "u": ("Go up", doGo), "d": ("Go down", doGo), "l": ("Go left", doGo),
    "r": ("Go right", doGo), "q": ("Quit", doQuit)
  }
  
  # If at surface, can use the shop
  if atSurface(): 
    for item in shopItems(): game.cmds[item[0]] = ("%s) $%d %s"%item[:3], doBuy)
  # Otherwise, can restore a checkpoint
  else: game.cmds["e"] = ("Restore Checkpoint", doRestore)

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

  # After each move, make the player fall if appropriate
  fall()
  
  # If the miner has the relic, traps are active
  if game.relic: checkTraps()

def fall():
  if tileAt(game.miner_pos)=="H": return
  
  distance = 0
  
  while not solidAt(game.miner_pos.add(Vec2(0, 1))):
    game.miner_pos.y += 1
    distance += 1
    
  # Determine outcome of falling
  if distance > 3:
    print("You fall", distance*10, "feet, to your death!")
    restoreCheckpoint()
  elif distance > 0:
    print("You fall", distance*10, "feet!")

def checkTraps():
  # Spike traps
  if tileAt(game.miner_pos.add(Vec2( 1,  0)))=="<" or \
     tileAt(game.miner_pos.add(Vec2(-1,  0)))==">" or \
     tileAt(game.miner_pos.add(Vec2( 0, -1)))=="v" or \
     tileAt(game.miner_pos.add(Vec2( 0,  1)))=="^":    
    print("The spike trap springs out and kills you!")
    restoreCheckpoint()
  
  # Arrow traps
  shot = False
  for x in range(1, 10):
    if tileAt (game.miner_pos.add(Vec2(x, 0)))=="{": shot = True
    if solidAt(game.miner_pos.add(Vec2(x, 0))): break
  for x in range(1, 10):
    if tileAt (game.miner_pos.add(Vec2(-x, 0)))=="}": shot = True
    if solidAt(game.miner_pos.add(Vec2(-x, 0))): break
  if shot:
    print("An arrow shoots out of the arrow trap and kills you!")
    restoreCheckpoint()
      
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
    ladders = 0    
    while not solidAt(boulder[0].add(Vec2(0, 1)), "H@"):
      boulder[0].y += 1
      
      if tileAt(boulder[0])=="H":
        setTile(boulder[0], ".")
        ladders += 1
      
      if game.miner_pos.eq(boulder[0]):
        print("The falling boulder kills you!")
        restoreCheckpoint()
        return
      
    setTile(boulder[0], "0")
    if ladders > 0: print("The falling boulder destroys", ladders,
      "ladder" + (ladders!=1 and "s" or "") + "!")
    print("The falling boulder lands.")
  
  # Actually remove settled boulders from array
  for boulder in goners: game.live_boulders.remove(boulder)  

# The following functions, starting with "do," are commands the miner might
# execute.

def doQuit(move): game.quit = input("Are you sure? (Y/N) ").lower()=="y"

def doRestore(move): restoreCheckpoint()

def doBuy(move):
  for item in shopItems():
    if item[0]==move:
      if game.bank_money < item[1]: print("You can't afford it!")
      else:
        game.bank_money -= item[1]
        item[3](item[1])
  
def doGo(move):
  if move=="u": dir = Vec2( 0, -1)
  if move=="d": dir = Vec2( 0,  1)
  if move=="l": dir = Vec2(-1,  0)
  if move=="r": dir = Vec2( 1,  0)
    
  new_pos = game.miner_pos.add(dir)

  # If climbing, try to use a ladder
  if dir.y < 0 and tileAt(game.miner_pos)!="H":
    if game.ladders == 0:
      print("You can't go up because you don't have any ladders!")
      return
    if atSurface():
      print("You can't go up because you're already on the surface!")
      return
    game.ladders -= 1
    setTile(game.miner_pos, "H")
    print("You drop a ladder to climb.")
    
  # Don't move into impassable objects
  for b in [("0=", "boulder"), ("|-", "impassable wall"), \
            ("^v<>", "spike trap"), ("{}", "arrow trap")]:
    if tileAt(new_pos) in b[0]:
      print("You can't dig into %ss!"%b[1])
      return

  # Interact with stuff in the world
  if solidAt(new_pos, "H%"):  
    # Loose treasure
    if tileAt(new_pos) == "$":
      print("You found some treasure, worth $"+str(int(new_pos.y/5+1))+"!")
      game.carried_money += int(new_pos.y/5+1)
    # Treasure chest
    elif tileAt(new_pos) == "n":
      if random() < 0.5:
        print("You find $%d of treasure in the chest!" % (game.world_size.y*2))
        game.carried_money += game.world_size.y*2
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
  if not atSurface() and new_pos.y==-1: reachSurface()
  
  # Actually perform the move
  game.miner_pos = new_pos
  
  # Grab the relic if touched
  if tileAt(game.miner_pos)=="%": 
    game.relic = True
    setTile(game.miner_pos, ".")
    print("\n"+textwrap.fill(game.realm["relic"]))

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
    
  # Build a data structure of available items in the shop
  return [("b", 2**(game.light-2),       "Upgrade lamp brightness", buyLamp), \
          ("c", 2**(game.max_ladders-4), "Upgrade ladder capacity", buyLadder)]

def reachSurface():
  if game.relic:
    print(textwrap.fill(game.realm["exit"]))
    nextRealm()
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
  if p.y==game.world_size.y: return "-"
  if p.x==-1 or p.x==game.world_size.x: return "|"
  if p.x<-1 or p.x>game.world_size.x or p.y<0 or p.y>game.world_size.y:
    return " "
  return game.world[p.x][p.y]

# Barebones 2D Vector class; only the methods we need.
class Vec2:
  def __init__(_, x, y): _.x, _.y = x, y    
  def eq (_, v): return _.x==v.x and _.y==v.y
  def add(_, v): return Vec2(_.x+v.x, _.y+v.y)
  def clone(_): return Vec2(_.x, _.y)
  
# Python idiom to call main() if this module is being executed directly
if __name__=="__main__": main()

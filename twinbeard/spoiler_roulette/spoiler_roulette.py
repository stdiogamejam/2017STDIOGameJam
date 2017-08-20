import json
import random

def main():
  # Read and shuffle spoiler list
  with open("spoilers.json", "r") as f: spoilers = json.load(f)
  random.shuffle(spoilers)
  
  print("Welcome to Spoiler Roulette!\n")
  
  # Gather player names
  players = []
  while True:
    name = input("Enter the name of the "+(players==[] and "first" or "next")+
      " player, or press enter if done: ")
    if name!="": 
      if name not in players: players.append(name)
      else:
        print("Two %ss?! I can't deal with that. One of you pick a nickname." \
              % name)
    else:
      if len(players) < 2: print("There must be at least two players!")
      else: break
      
  print("\nIf you make it out of here, you'll be legends.")
  
  # Go through players in random order
  random.shuffle(players)  
  player_index = 0
  spoiler_index = 0
  
  while len(players)>1:
    player = players[player_index]
    
    print("\nPlayers left:", ", ".join(players))
    print(player+", you're up. Everyone else close their eyes.")    
    input("Press enter when you're ready: ")
    print("\n"+spoilers[spoiler_index])
    
    # We have no choice but to trust players as to whether they were spoiled.
    print("\nWas that a spoiler?")
    print("  A. Yes.")
    print("  B. No, I knew it already.")    
    print("  C. No, I don't know what it means.")
    
    # Keep asking for input until they give us a legal answer
    result = ""
    while len(result)!=1 or result not in "abc":
      result = input("A, B or C? ").strip().lower()
    
    # Print 50 new lines so that the spoiler is hopefully off screen.
    print("\n"*50)
    
    if result=="a":
      print(player+", you're out!")
      players.remove(player)
    elif result=="b":
      print(player+", you're safe for now...")
    else:
      print("Well, maybe someday.")
            
    print("\nOkay, you can all look now.")
    
    # Select the next player, wrapping around if need be.
    player_index  = (player_index +1)%len(players)
    
    # Select the next spoiler -- if we run out, also re-shuffle.
    spoiler_index += 1    
    if spoiler_index >= len(spoilers):
      spoiler_index = 0
      random.shuffle(spoilers)

  print("\n"+players[0], "got away unspoiled!")
    
if __name__=="__main__": main()

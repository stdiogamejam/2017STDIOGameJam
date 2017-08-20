### BATTLESHIP ##################
# Author: Racso (Oscar Fernando Gomez) - racso.co, github.com/racsoth, bitbucket.com/racsoth
# Developed during the STDIO Game Jam 2017, Aug 19th and 20th
# License: MIT - https://opensource.org/licenses/MIT
#################################

# CONFIG: CHANGE THOSE TWO VARIABLES TO CONFIG YOUR GAME.
shiplen = [3, 3, 4] #the length of the ships in play. [2, 3, 3] means "one ship of length 2 and two of length 3".
size = 5 # the size of the board. 5 means "5x5".

### NOTES ABOUT THE CODE#########
# This code is aimed at people who don't know Object Oriented Programming. Therefore, it doesn't use objects.
# It does, however, use some Python features such as generators and list comprehensions to achieve some objectives with cleaner code.
#
# Ships are lists that contain tuples (immutable lists). Each tuple contains 3 elements: x and y coordinates, and a value representing if the piece has been hit or not.
#
# Extra comments about the code.
# [1] Infinite loops like this one need to be treated with care. Some programmers say they are bad programming, some others don't see the problem with them. In the author's opinion, they are useful to simplify code in languages without do-while loops like Python.
# [2] Python doesn't have arrays or matrices.
#################################

from random import randint as rand

def randomShip(boardSize, shipSize):
    # This function generates a new random ship inside the board.
    ship = []
    orientation = "H" if rand(1,2)==1 else "V" # random orientation: Horizontal or Vertical.

    # Now, whe clamp the possible starting location of the ships according to their orientation, to avoid it going out of the board:
    maxx = boardSize-1 if orientation == "V" else boardSize-shipSize
    maxy = boardSize-1 if orientation == "H" else boardSize-shipSize
    
    ship.append([rand(0, maxx), rand(0, maxy), False]) # adding a first piece in a random position.
    
    for i in range(1, shipSize):
        if orientation == "H":
            newPiece = [ship[0][0]+i, ship[0][1], False] # If horizontal, we vary the x coordinate of the first piece to create more.
        else:
            newPiece = [ship[0][0], ship[0][1]+i, False] # If vertical, we vary the y coordinate of the first piece to create more.
        ship.append(newPiece) #we add the new piece.
        
    return ship

def shipOverlaps(ship, otherShips):
    # This function checks if a ship overlaps with other ships or not.
    for piece in allPieces(otherShips):
        if piece in ship:
            return True
    return False

def printBoard(boardSize, ships, shots):
    # This function prints a board.
    print("RADAR STATUS:\n")
    board = [[None]*boardSize for i in range(boardSize)] # This creates an empty "matrix"of size boardSize x boardSize. [2]
    for r in range(boardSize):
        for c in range(boardSize):
            label = "[    ]" if [c, r] in shots else "[ " + chr(65+c)+chr(65+r) + " ]"
            board[r][c] = label # We fill the board with labels.

    for piece in allPieces(ships):
        if piece[2]==True:
            board[piece[1]][piece[0]] = "[ !! ]"

    for row in board:
        print(" ".join(row))

def printIntel(boardSize, ships, shots):
    # This function prints some intel about the status of the game.
    print("INTEL STATUS:\n")
    for i in range(len(ships)):
        print("Ship " + str(i+1) +" (size " + str(len(ships[i]))+"): " + shipStatus(ships[i]))
        
def shipStatus(ship):
    # This function checks the status of a ship: 0 = OK, 1 = HIT, -1 = SUNK
    hits = 0
    for piece in ship:
        if piece[2]==True: hits += 1
    if hits == 0: return "NOT HIT YET"
    if hits >= len(ship): return "SUNK"
    return "HIT"

def allPieces(ships):
    # This function is an iterator. It's used to iterate over all the pieces in all the ships.
    for ship in ships:
        for piece in ship:
            yield piece

def won(ships):
    for piece in allPieces(ships):
        if piece[2]==False: return False
    return True

def PlayGame(shiplen, size):
    # This is the main function. It's called for playing a game.

    print("STARTING NEW GAME\n")
    
    shots = [] # Shots made.
    # Let's add the ships to the board.
    ships = []
    for l in shiplen:
        while True: # An infinite loop? See [1].
            newShip = randomShip(size,l)
            if shipOverlaps(newShip, ships) == False: break
        ships.append(newShip)

    # Let the fun begin!
    while True:

        # Now, let's read a command until is valid.
        while True:
            print("===================================")
            printBoard(size, ships, shots)
            print("")
            printIntel(size, ships, shots)
            print("===================================\n")

            try:
                command = input("Your command, sir? [Q to Quit] ").upper()
                if command=="Q": quit()
                targetCoordinates = [ord(char)-65 for char in command] # We take every character in the command, take its ASCII code and convert it to a coordinate.
                if len(targetCoordinates) != 2: raise # If we couldn't get exactly 2 coordinates from the input, we got an error.
                break
            except:
                print("Negative, sir.") # If the command is invalid somehow, simply say so and try again.

        # Clear the screen. There are other ways to try to do this, each with advantages and disadvantages.
        print("\n" * 100)
        
        shots.append(targetCoordinates)

        # Check if we hit something.
        print("Command: " + command)
        hit = False
        for piece in allPieces(ships):
            if piece[0]==targetCoordinates[0] and piece[1]==targetCoordinates[1]:
                print("Target hit, sir!")
                piece[2] = True
                hit = True
                break
        if hit == False:
            print("Missed, sir.")
        if won(ships):
            print("Targets terminated, sir. We've won the battle!")
            print("Number of shots: " + len(shots) + ". Awesome! Try to improve your own record next time!")
            return
        print("")

print("WELCOME TO BATTLESHIP")
PlayGame(shiplen, size)

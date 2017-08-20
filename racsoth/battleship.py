from random import randint as rand
# CONFIG
shiplen = [2, 3, 3] #the length of the ships in play. [2, 3, 3] means "one ship of length 2 and two of length 3".
size = 5# the size of the board. 5 means "5x5".


########## BATTLESHIP ###########
# This code is aimed at people who don't know Object Oriented Programming. Therefore, it doesn't use objects.
# Ships are lists that contain tuples (immutable lists). Each tuple contains 3 elements: x and y coordinates, and a value representing if the piece has been hit or not.
#################################


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

def insideTheBoard(piece, size):
    return 0<=piece[0]<size and 0<=piece[1]<size # both coordinates are between 0 and size-1? Python allows this kind of multi-comparisons.

def shipOverlaps(ship, otherShips):
    # This function checks if a ship overlaps with other ships or not.
    for other in otherShips:
        for piece in ship:
            if piece in other:
                return True
    return False

def printBoard(boardSize, ships):
    board = [[None]*boardSize for i in range(boardSize)] # This creates an empty "matrix"of size boardSize x boardSize. [2]
    for r in range(boardSize):
        for c in range(boardSize):
            label = "[    ]" if [c, r] in shots else "[ " + chr(65+c)+chr(65+r) + " ]"
            board[r][c] = label # We fill the board with labels.
            
    for ship in ships:
        for piece in ship:
            if piece[2]==True:
                board[piece[0]][piece[1]] = "[ !! ]"

    for row in board:
        print(" ".join(row))
    
shots = [] # shots made.

# Let's add the ships to the board.
ships = []
for l in shiplen:
    while True: # An infinite loop? See [1].
        newShip = randomShip(size,l)
        if shipOverlaps(newShip, ships) == False: break
    ships.append(newShip)

# Let the fun begin!
while True:
    printBoard(size, ships)
    #printIntel(ships)

    # Now, let's read a command until is valid.
    while True:
        print(shots)
        print(ships)
        try:
            command = input("Your command, sir? ").upper()
            if command=="Q": quit()
            targetCoordinates = [ord(char)-65 for char in command] # We take every character in the command, take its ASCII code and convert it to a coordinate.
            if len(targetCoordinates) != 2: raise
            break
        except:
            print("Negative, sir.") # if the command is invalid somehow, simply say so and try again.

    shots.append(targetCoordinates)
    
    hit = False
    for ship in ships:
        for piece in ship:
            if piece[0]==targetCoordinates[0] and piece[1]==targetCoordinates[1]:
                print("Target hit, sir!")
                piece[2] = True
                hit = True
                break
    if hit == False:
        print("Missed, sir.")

# Extra comments
# [1] Infinite loops like this one need to be treated with care. Some programmers say they are bad programming, some others don't see the problem with them. In the author's opinion, they are useful to simplify code in languages without do-while loops like Python.
# [2] Python doesn't have arrays or matrices.

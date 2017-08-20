from random import randint as rand

def Game():

    def printBoard():
        for r in range(size):
            print("   ".join(["/"+item+"\\" for item in board[r]]))
            print("   ".join(["\\"+str(num).center(6)+"/" for num in range(r*size, (r+1)*size)]))

    def xy(cell):
        return cell % size, cell//size

    def cell(x,y):
        return y*size+x
        
    def takenCells(initial):
        initialPos = xy(initial)
        taken = { initial }
        for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
            for dif in range(0, size):
                pos = (initialPos[0]+dif*direction[0],initialPos[1]+dif*direction[1])
                if not(0<=pos[0]<size and 0<=pos[1]<size) or board[pos[1]][pos[0]]!=board[initialPos[1]][initialPos[0]]: break
                taken.add(cell(pos[0],pos[1]))
        return taken
        

    size = 5
    board = []

    items = ["Goblin", "Potion", "Regen.", "Attack", "Shield"]

    for r in range(size):
        row = []
        for c in range(size):
            row.append(items[rand(0,len(items)-1)])
            
        board.append(row)

    printBoard()
    command = int(input("Cell number to Attack / Take: "))

    print(takenCells(command))
    #taken = takenCells(command)
    #removeFromBoard(taken)

Game()


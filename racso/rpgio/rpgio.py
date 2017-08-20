from random import randint as rand

GOBLIN, POTION, MONEY, TRAP, EMPTY = "Goblin", "Potion", " Gold ", " Trap ", "      "
items = [GOBLIN, POTION, MONEY, TRAP]

def Game():

    def printBoard():
        for r in range(size):
            print(" ".join(["/ "+item+" \\" for item in board[r]]))
            print(" ".join(["\\ "+str(num).center(6)+" /" for num in range(r*size, (r+1)*size)]))

    def printStats():
        nonlocal hp, gold
        print("Current round: " + str(round))
        print("Your HP: " + str(hp))
        print("Your gold: " + str(gold))
    
    def xy(cell):
        return cell % size, cell//size

    def cell(x,y):
        return y*size+x
        
    def takenCells(initial):
        initialPos = xy(initial)
        taken = { initialPos }
        for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
            for dif in range(1, size):
                pos = (initialPos[0]+dif*direction[0], initialPos[1]+dif*direction[1])
                if not(0<=pos[0]<size and 0<=pos[1]<size) or board[pos[1]][pos[0]]!=board[initialPos[1]][initialPos[0]]: break
                taken.add(pos)
        return taken

    def processCells(cells):
        nonlocal hp, gold
        element = board[cells[0][1]][cells[0][0]]
        amount = len(cells)
        if element==GOBLIN:
            print("You killed %s goblins!" % amount)
        elif element==POTION:
            print("You drank %s potions!" % amount)
            hp += amount
        elif element==MONEY:
            print("You picked %s gold!" % amount)
            gold += amount
        elif element==TRAP:
            print("You disabled %s traps." % amount)

    def removeFromBoard(cells):
        for cell in cells:
            board[cell[1]][cell[0]]=EMPTY
        while True:
            changeMade = False
            for row in range(size-1, 0, -1):                
                for col in range(size):
                    if board[row][col]==EMPTY and board[row-1][col]!=EMPTY:
                        changeMade, board[row-1][col], board[row][col] = True, EMPTY, board[row-1][col]
            if changeMade == False: break
        return

    def receiveDamage():
        nonlocal hp
        goblins = sum([row.count(GOBLIN) for row in board])
        print("You are attacked by %s goblins! Each one does 1 damage!" % goblins)
        hp -= goblins

    def fillBoard():
        for r in range(size):
            for c in range(size):
                if board[r][c]==EMPTY: board[r][c] = items[rand(0,len(items)-1)]
        
    size = 5
    board = [[EMPTY]*size for i in range(size)]
    fillBoard()

    gold = 0
    hp = 15
    round = 1

    while True:
        printBoard()
        printStats()
        while True:
            try:
                command = int(input("Cell number to Attack / Take: "))
                if command<0 or command>=size*size-1: raise
                break
            except:
                print("Invalid command.")

        print("\n"*3)
        print("="*10)
        print("Your selection: cell %s" % command)
        taken = list(takenCells(command))
        processCells(taken)
        removeFromBoard(taken)
        receiveDamage()
        if hp<=0:
            print("YOU DIED!\n")
            print("You collected " + str(gold) + " GOLD in " + str(turns))
            return
        print("")
        print("Updating the board (removing your cells, letting cells fall to fill the empty spaces, filling the board with new cells)...")
        print("")
        fillBoard()
        round += 1

Game()


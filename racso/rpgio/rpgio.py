### RPG.io ##################
# Author: Racso (Oscar Fernando Gomez) - racso.co, github.com/racso, bitbucket.com/racsoth
# Developed during the STDIO Game Jam 2017, Aug 19th and 20th
# License: MIT - https://opensource.org/licenses/MIT
#################################


from random import randint as rand

GOBLIN, POTION, MONEY, TRAP, EMPTY = "Goblin", "Potion", " Gold ", " Trap ", "      "

def Game():
    global GOBLIN, POTION, MONEY, TRAP, EMPTY
    def printBoard():
        nonlocal mode
        for r in range(size):
            if mode==1:
                print(" ".join(["/ "+item+" \\" for item in board[r]]))
                print(" ".join(["\\ "+str(num).center(6)+" /" for num in range(r*size, (r+1)*size)]))
            else:
                print("".join([item for item in board[r]]) + "   " + str(r*size)+"-"+str((r+1)*size-1))

    def printStats():
        nonlocal hp, gold, turn
        print("Current round: " + str(turn))
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


    def read(prompt, error, minimum, maximum):
        while True:
            try:
                command = int(input(prompt))
                if command<minimum or command>maximum: raise
                return command
            except:
                print(error)
        
    print(
 '''
  _____    _____     _____       _       
 |  __ \  |  __ \   / ____|     (_)      
 | |__) | | |__) | | |  __       _  ___  
 |  _  /  |  ___/  | | |_ |     | |/ _ \ 
 | | \ \  | |      | |__| |  _  | | (_) |
 |_|  \_\ |_|       \_____| (_) |_|\___/
 By RACSO. http://racso.co\n\n
 ''')
    print("You're exploring a dangerous dungeon to collect GOLD ($). Be aware of GOBLINS (@)! If you are hurt, drink POTIONS (+) to heal. You may find TRAPS (_) which you can disable easily to make for exploring.")
    print("Each turn, you interact with a cell in the board PLUS every other cell of the same type horizontally or vertically connected with it.")
    print("Those cells are removed from the board, the remaining cells fall to fill the blank spaces and new cells appear to fill the board.")
    print("")
    print("GRAPHIC MODES:")
    print("1. Basic. Ideal for new players.")
    print("2. Minimum. Ideal for veterans for faster gameplay.")
    mode = read("Select mode: ","Invalid mode",1,2)
    
    if mode==2:
        GOBLIN, POTION, MONEY, TRAP, EMPTY = "@", "+", "$", "_", ""

    items = [GOBLIN, POTION, MONEY, TRAP]
    
    print("\n"*100)
    
    size = 5
    board = [[EMPTY]*size for i in range(size)]
    fillBoard()

    gold = 0
    hp = 15
    turn = 1

    while True:
        printBoard()
        print("")
        printStats()
        print("")
        command = read("Cell number to interact with: ", "Invalid command.", 0, size*size-1)
        
        print("\n"*3)
        print("="*10)
        print("Your selection: cell %s" % command)
        taken = list(takenCells(command))
        processCells(taken)
        removeFromBoard(taken)
        receiveDamage()
        if hp<=0:
            print("YOU DIED!\n")
            print("You collected " + str(gold) + " GOLD in " + str(turn) + " turns.")
            return
        print("")
        print("Updating the board (removing your cells, letting cells fall to fill the empty spaces, filling the board with new cells)...")
        print("")
        fillBoard()
        turn += 1

Game()


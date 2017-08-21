### RPG.io ##################
# Author: Racso (Oscar Fernando Gomez) - racso.co, github.com/racso, bitbucket.com/racsoth
# Developed during the STDIO Game Jam 2017, Aug 19th and 20th
# License: MIT - https://opensource.org/licenses/MIT
#################################

from random import randint as rand


class Game():

    def printBoard(self):
        for r in range(self.size):
            if self.mode == 1:
                print(
                    " ".join(["/ " + item + " \\" for item in self.board[r]]))
                print(" ".join(["\\ " + str(num).center(6) +
                                " /" for num in range(r * self.size, (r + 1) * self.size)]))
            else:
                print("".join([item for item in self.board[r]]) + "   " +
                      str(r * self.size) + "-" + str((r + 1) * self.size - 1))

    def printStats(self):
        print("Current round: " + str(self.turn))
        print("Your HP: " + str(self.hp))
        print("Your Gold: " + str(self.gold))

    def takenCells(self, initial):
        initialPos = initial % self.size, initial // self.size
        taken = {initialPos}
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for dif in range(1, self.size):
                pos = (initialPos[0] + dif * direction[0],
                       initialPos[1] + dif * direction[1])
                if not(0 <= pos[0] < self.size and 0 <= pos[1] < self.size) or self.board[pos[1]][pos[0]] != self.board[initialPos[1]][initialPos[0]]:
                    break
                taken.add(pos)
        return taken

    def processCells(self, cells):
        element, amount = self.board[cells[0][1]][cells[0][0]], len(cells)
        if element == self.GOBLIN:
            print("You killed %s goblins!" % amount)
        elif element == self.POTION:
            print("You drank %s potions!" % amount)
            self.hp += amount
        elif element == self.MONEY:
            print("You picked %s gold!" % amount)
            self.gold += amount
        elif element == self.TRAP:
            print("You disabled %s traps." % amount)

    def removeFromBoard(self, cells):
        for cell in cells:
            self.board[cell[1]][cell[0]] = self.EMPTY
        while True:
            changeMade = False
            for row in range(self.size - 1, 0, -1):
                for col in range(self.size):
                    if self.board[row][col] == self.EMPTY and self.board[row - 1][col] != self.EMPTY:
                        changeMade, self.board[row - 1][col], self.board[row][col] = True, self.EMPTY, self.board[row - 1][col]
            if changeMade == False:
                break

    def receiveDamage(self):
        goblins = sum([row.count(self.GOBLIN) for row in self.board])
        print("You are attacked by %s goblins! Each one does 1 damage!" % goblins)
        self.hp -= goblins

    def fillBoard(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == self.EMPTY:
                    self.board[r][c] = self.items[rand(0, len(self.items) - 1)]

    def read(self, prompt, error, minimum, maximum):
        while True:
            try:
                command = int(input(prompt))
                if command < minimum or command > maximum:
                    raise
                return command
            except:
                print(error)

    def run(self):
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
        self.mode = self.read("Select mode: ", "Invalid mode", 1, 3)

        if self.mode == 1:
            self.GOBLIN, self.POTION, self.MONEY, self.TRAP, self.EMPTY = "Goblin", "Potion", " Gold ", " Trap ", "      "
        else:
            self.GOBLIN, self.POTION, self.MONEY, self.TRAP, self.EMPTY = "@", "+", "$", "_", ""
        self.items = [self.GOBLIN, self.POTION, self.MONEY, self.TRAP]

        print("BOARD SIZE & DIFFICULTY:\n1. Small (5x5, easy, recommended for learning)\n2. Medium (7x7, normal)\n3. Big (10x10, hard)\n4. Fantastic (14x14, very hard)")
        self.size = self.read("Select size: ", "Invalid size", 1, 4)

        self.hp = 30 * self.size**2
        self.size = 4 + (self.size * (self.size + 1)) // 2

        self.board = [[self.EMPTY] * self.size for i in range(self.size)]
        self.fillBoard()

        self.gold = 0
        self.turn = 1

        print("\n" * 100)

        while True:
            self.printBoard()
            print("")
            self.printStats()
            print("")
            command = self.read("Cell number to interact with: ", "Invalid command.", 0, self.size * self.size - 1)
            print("\n" * 3)
            print("=" * 10)
            print("Your selection: cell %s" % command)
            taken = list(self.takenCells(command))
            self.processCells(taken)
            self.removeFromBoard(taken)
            self.receiveDamage()
            if self.hp <= 0:
                print("YOU DIED!\n")
                print("You collected " + str(self.gold) + " gold in " + str(self.turn) + " turns.")
                return
            print("")
            print("Updating the board (removing your cells, letting cells fall to fill the empty spaces, filling the board with new cells)...")
            print("")
            self.fillBoard()
            self.turn += 1


Game().run()

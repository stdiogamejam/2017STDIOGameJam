
#
# Created for STDIO Jam 2017 by Emmanuel Ah-kouen (https://github.com/dyoxyne)
#

# Used to shuffle the cards
from random import shuffle
# Used for Regular Expressions
import re
# Used for Enumerations (optional)
from enum import Enum

# Used for displaying the game introduction in the console
INTRODUCTION = '''
=============================================================
=============================================================
  ____ _                     ____  _                       _ 
 / ___| | _____   _____ _ __|  _ \(_)___  ___ __ _ _ __ __| |
| |   | |/ _ \ \ / / _ \ '__| | | | / __|/ __/ _` | '__/ _` |
| |___| |  __/\ V /  __/ |  | |_| | \__ \ (_| (_| | | | (_| |
 \____|_|\___| \_/ \___|_|  |____/|_|___/\___\__,_|_|  \__,_|
=============================================================
=============================================================


The goal in Clever Discard is to discard all cards onto two discard stacks.

There are two types of discard stacks:
* Ascending order stack (from 1 to 100)
* Descending order stack (from 100 to 1)

Each turn, the player can:
* Draw new cards until his/her hands are full (8 cards)
* Place a card to a discard stack
* Remove a card from the game

The game ends when there are no more cards left (in the deck / player hands).


Commands list:
1/ "q" to quit the game
2/ "d" to draw cards
3/ "a{card}" to put {card} from hands onto the stack A (ascending order)
4/ "b{card}" to put {card} from hands onto the stack B (descending order)
5/ "r{card}" to remove {card} from the game
You can execute multiple commands by inserting "," between each command.

Examples:
* "a25" to put the card (value 25) onto the stack A
* "r80" to remove the card (value 80) from the game
* "a10,b33,d" to put the card (value 10) to the stack A, to put the card (value 33) to the stack B and then draw cards

Remarks:
* You cannot remove a card that is not in your hands
* The maximum cards you can have in your hands is 8


=============================================================
'''

# Enumeration about the stack type
class StackType(Enum):
    ASC = 1 # Ascending order
    DESC = 2 # Descending order

class Stack:
    # Stack class constructor
    def __init__(self, stackType, initialCard):
        self.stackType = stackType
        self.cards = [initialCard]

    # Add a card onto the stack
    # The card will be added only if it follows the ordering rules according to the stack type
    def add(self, card):
        if (self.stackType == StackType.ASC):
            if (card > self.getLastCard()):
                self.cards.append(card)
                return True
        elif (self.stackType == StackType.DESC):
            if (card < self.getLastCard()):
                self.cards.append(card)
                return True

        print("You cannot add the card", card, "to the discard stack!")
        return False

    # Get the last discarded card
    def getLastCard(self):
        cardsCount = len(self.cards)
        return self.cards[cardsCount-1]

    # Display the stack status in the console
    def display(self):
        if (self.stackType == StackType.ASC):
            text = "Stack A (ascending) :"
        elif (self.stackType == StackType.DESC):
            text = "Stack B (descending):"

        print(text, self.getLastCard())

class Game:
    # Represents the maximum cards in the hands
    MAX_HANDS_CARDS = 8
    # Represents the number of cards that can be removed
    MAX_REMOVED_CARDS = 5
    # Represents the lowest card number
    MIN_CARD = 1
    # Represents the highest card number
    MAX_CARD = 100

    # Game class constructor
    def __init__(self):
        # Used to track how many times the player used the remove card ability
        self.removedCards = 0
        # Initialize deck, stacks and hands
        # A game is composed of:
        # - one player hands
        # - two discard stacks
        # - one cards deck
        self.initializeDeck()
        self.initializeStacks()
        self.initializeHands()

    # Initialize the deck
    def initializeDeck(self):
        self.deck = [];
        # Create cards from [MIN_CARD+1, MAX_CARD-1]
        for i in range(self.MIN_CARD + 1, self.MAX_CARD):
            self.deck.append(i)
        # Shuffle the cards
        shuffle(self.deck)

    # Initialize the stack A and B
    def initializeStacks(self):
        self.stacks = []
        # Represents stack A (ascending order) and put MIN_CARD as the first card
        self.stacks.append(Stack(StackType.ASC, self.MIN_CARD))
        # Represents stack B (descending order) and put MAX_CARD as the first card
        self.stacks.append(Stack(StackType.DESC, self.MAX_CARD))

    # Initialize player hands
    def initializeHands(self):
        self.hands = []
        # Take MAX_HANDS_CARDS cards into the player hands
        for i in range(self.MAX_HANDS_CARDS):
            self.hands.append(self.deck.pop())

    # Used for knowing if the game is over or not
    def isGameOver(self):
        # The game is over if the deck and the player hands are both empty
        return ((len(self.deck) == 0) and (len(self.hands) == 0))

    # Execute a new turn
    def nextTurn(self):
        # Display the current game status
        self.display()
        # Ask for player input
        inputTemp = input("What do you want to do? ").lower()
        # Split the player input by ,
        # This allows to write many actions on the same line
        actions = inputTemp.split(",")
        for i in range(len(actions)):
            action = actions[i]
            # Check if the player wrote a quit action
            m = re.match("q|quit", action)
            if m:
                print("...")
                return
            # Check if the player wrote a draw action
            m = re.match("d|draw", action)
            if m:
                self.drawCards()
            # Check if the player wrote a place card action
            m = re.match("a(\d+)", action)
            if m:
                # m.group(1) represents the card value
                self.placeCard(StackType.ASC, int(m.group(1)))
            # Check if the player wrote a place card action
            m = re.match("b(\d+)", action)
            if m:
                # m.group(1) represents the card value
                self.placeCard(StackType.DESC, int(m.group(1)))
            # Check if the player wrote a draw card action
            m = re.match("r(\d+)", action)
            if m:
                self.removeCard(int(m.group(1)))
            # Check if the player won the game
            if self.isGameOver():
                print("You won!")
                return
        # Recursively call nextTurn to continue the game until the players quits or wins
        self.nextTurn()

    # Place a card onto a discard stack
    def placeCard(self, stackType, card):
        # Check if we are placing a card that is currently in the hands
        if card in self.hands:
            index = self.hands.index(card)
            if stackType == StackType.ASC:
                stack = self.stacks[0]
            elif stackType == StackType.DESC:
                stack = self.stacks[1]

            # Place the card onto the discard stack according to the ordering rules
            if stack.add(card):
                # Remove the card from the hands only if we can place the card
                self.hands.pop(index)
        return

    # Remove a card 
    def removeCard(self, card):
        # Check if we can still remove cards
        if self.MAX_REMOVED_CARDS <= self.removedCards:
            print("You cannot remove anymore card!")
            return
        # Check if we are removing a card that is currently in the hands
        if card in self.hands:
            # Remove the card
            index = self.hands.index(card)
            self.hands.pop(index)
            self.removedCards += 1
        else:
            print("You cannot remove card", card, "because it is not in your hands!")

    # Draw cards
    def drawCards(self):
        # Check how many cards we need to draw
        delta = min(self.MAX_HANDS_CARDS - len(self.hands), len(self.deck))
        if delta > 0:
            print("You drew", delta, "card(s)!")
            for i in range(delta):
                self.hands.append(self.deck.pop())

    # Display the game status in the console
    def display(self):
        print("---------------------------")
        for i in range(len(self.stacks)):
            self.stacks[i].display()

        print("Cards:", len(self.deck))
        print("Remove (left):", self.MAX_REMOVED_CARDS - self.removedCards)
        print("Hands:", self.hands)
        print("---------------------------")

# Main entry point of the game
def main():
    # Display the Logo and How To Play
    print(INTRODUCTION)
    # Instantiate and start a new game
    game = Game()
    game.nextTurn()

# Start the game
main()


from enum import Enum
from random import shuffle
import re

class StackType(Enum):
    ASC = 1
    DESC = 2

class Stack:
    def __init__(self, stackType, initialCard):
        self.stackType = stackType
        self.cards = [initialCard]

    def add(self, card):
        if (self.stackType == StackType.ASC):
            if (card > self.getLastCard()):
                self.cards.append(card)
                return True
        elif (self.stackType == StackType.DESC):
            if (card < self.getLastCard()):
                self.cards.append(card)
                return True

        print("Cannot be added!")
        return False

    def getLastCard(self):
        cardsCount = len(self.cards)
        return self.cards[cardsCount-1]

    def display(self):
        text = ""
        if (self.stackType == StackType.ASC):
            text = "Stack A (ascending): "
        elif (self.stackType == StackType.DESC):
            text = "Stack B (descending):"

        print(text, self.getLastCard())

class Game:
    MAX_HANDS_CARDS = 8
    MAX_DISCARDS = 5
    MIN_CARD = 1
    MAX_CARD = 50

    def __init__(self):
        self.removedCards = 0
        self.initializeDeck()
        self.initializeStacks()
        self.initializeHands()

    def initializeDeck(self):
        self.deck = [];
        for i in range(self.MIN_CARD + 1, self.MAX_CARD):
            self.deck.append(i)
        shuffle(self.deck)

    def initializeStacks(self):
        self.stacks = []
        self.stacks.append(Stack(StackType.ASC, self.MIN_CARD))
        self.stacks.append(Stack(StackType.DESC, self.MAX_CARD))

    def initializeHands(self):
        self.hands = []
        for i in range(self.MAX_HANDS_CARDS):
            self.hands.append(self.deck.pop())

    def isGameOver(self):
        return ((len(self.deck) == 0) and (len(self.hands) == 0))

    def nextTurn(self):
        self.display()

        inputTemp = input("What do you want to do? ").lower()
        actions = inputTemp.split(",")

        for i in range(len(actions)):
            action = actions[i]

            m = re.match("q|quit", action)
            if m:
                print("Quit")
                return

            m = re.match("d|draw", action)
            if m:
                self.drawCards()

            m = re.match("a(\d+)", action)
            if m:
                self.placeCard(StackType.ASC, int(m.group(1)))

            m = re.match("b(\d+)", action)
            if m:
                self.placeCard(StackType.DESC, int(m.group(1)))

            m = re.match("r(\d+)", action)
            if m:
                self.removeCard(int(m.group(1)))

            if self.isGameOver():
                print("You won!")
                return

        self.nextTurn()

    def placeCard(self, stackType, card):
        if card in self.hands:
            index = self.hands.index(card)
            if stackType == StackType.ASC:
                stack = self.stacks[0]
            elif stackType == StackType.DESC:
                stack = self.stacks[1]

            if stack.add(card):
                self.hands.pop(index)
        return

    def removeCard(self, card):
        if self.MAX_DISCARDS <= self.removedCards:
            return

        if card in self.hands:
            index = self.hands.index(card)
            self.hands.pop(index)
            self.removedCards += 1;

    def drawCards(self):
        delta = min(self.MAX_HANDS_CARDS - len(self.hands), len(self.deck))
        for i in range(delta):
            self.hands.append(self.deck.pop())

    def display(self):
        print("=================")
        for i in range(len(self.stacks)):
            self.stacks[i].display()

        print("Cards (left): ", len(self.deck))
        print("Remove (left): ", self.MAX_DISCARDS - self.removedCards)
        print("Hands: ", self.hands)
        print("=================")

def main():
    print("Welcome!")
    game = Game()
    game.nextTurn()
    return

# Start the game
main()

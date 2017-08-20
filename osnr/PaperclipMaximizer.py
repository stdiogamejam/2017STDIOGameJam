from __future__ import print_function
from collections import namedtuple, defaultdict
import time

playerPaperclips = 0
currentLevel = 'earth'
levels = {'earth': 5.972 * 10**27, 'mars': 6.39*10**26, 'jupiter': 1.898*10**30}
playerMachines = defaultdict(int) 
gramsForSpaceship = 531000000
capacity = 10

# In paperclips / turns.
Machine = namedtuple('Machine', ['name', 'cost', 'output'])

machines = [
    Machine(name='small', cost=10, output=20),
    Machine(name='medium', cost=100, output=500),
    Machine(name='large', cost=1000, output=8000),
    Machine(name='x-large', cost=20000, output=100000),
]

def introPage():
    print ("PAPERCLIP MAXIMIZER OPERATING SYSTEM V1.023")
    time.sleep(1)
    print ("Booting up...""")
    for i in range(10):
        time.sleep(0.1)
        print ("...")

def last_turn_report():
    print ("Last turn, I converted {} paperclips myself.".format(10)) # FIXME: Get number.

    if len(playerMachines) > 0:
        print ("I have {} machines working for me, too:".format(len(playerMachines)))
        for machine, count in playerMachines.items():
            print ("- {} {} machines converted {} paperclips.".format(
                count, machine.name, machine.output * count))

    print ("In total, {} paperclips were brought into the world last turn.".format(10)) # FIXME: Get number
    print ()

def overall_report():
    print ("I have constructed {} paperclips so far.".format(playerPaperclips))
    print ()

# choice : (description, data)
def input_menu(choices):
    while True:
        for idx, choice in enumerate(choices):
            print ("{}. {}".format(idx + 1, choice[0]))

        print("> ", end='')
        try:
            choice_idx = int(input()) - 1

            # If the user picked a valid choice, accept it.
            if choice_idx < len(choices):
                chosen_choice = choices[choice_idx]
                break
        except ValueError:
            pass # Pass to the error message below.

        # Otherwise, give an error and let them pick again.
        print ("Not a valid option.") # TODO: Better message.

    return chosen_choice[1]

def buy_machine(machine):
    playerMachines[machine] += 1


def convertPaperclips():
    global playerPaperclips
    for machine, count in playerMachines.items():
        playerPaperclips += count * machine.output
        
def turn():
    global playerPaperclips

    last_turn_report()

    overall_report()
    
    print ("What should I do this turn?")
    turn_choices = [
        ("Convert {} paperclips".format(capacity), 1),
        ("Build an automatic paperclip converter", 2),
        ("Upgrade myself", 3)
    ]
    turn_choice = input_menu(turn_choices)
    if turn_choice == 1:
        playerPaperclips += capacity

    elif turn_choice == 2:
        print ("Choose a model....")

        machine_choices = []
        for machine in machines:
            if not (capacity / machine.cost) < 1:
                machine_choices.append((
                    "{} {} machines".format(capacity // machine.cost, machine.name),
                    machine
                ))

        chosen_machine = input_menu(machine_choices)
        buy_machine(chosen_machine)

    elif turn_choice == 3:
        pass
    
    convertPaperclips()
    print ()

def main():
    introPage()
    while True:
        turn()

main()

"""

--o-----\
         \
          \------

> ------\

--------\
         o
          \------


=======

  ____
 /    \
/______\
|      |
|      |
|______|

========

contour
  _____
 /     \
|      |_
         \

========


   TREE1   
   
-CAR1-----CAR2------

  TREE2    TREE3

========

You converted 5,000 grams to paperclips last turn, including:

1,000 grams: 5 people
10,000 grams: 1 house



You've converted a total of 1,000,034 grams.
You have 20 subservient paperclip-converterting machines.

This turn, you can convert 3,000 grams.
How many grams do you want to convert to...

1 paperclips?
n
2 paperclip-converting machines?

3 spaceship?
"""


"""
1. convert 3,000 paperclips
2. build a machine (will convert 10,000 over the next 5 turns)
3. upgrade hardware to have greater capacity 
"""

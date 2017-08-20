from collections import namedtuple
import time

total_grams_converted = 0
current_level = 'earth'
levels = {'earth': 5.972 * 10**27, 'mars': 6.39*10**26, 'jupiter': 1.898*10**30}
grams_for_spaceship = 531000000
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

def turn():
    global total_grams_converted

    print ("I have constructed {} paperclips so far.".format(total_grams_converted))
    print ()

    print ("What should I do this turn?")
    print ("1. Convert {} paperclips".format(capacity))
    print ("2. Build an automatic paperclip converter")
    print ("3. Upgrade myself")
    choice = input()
    if choice == 1:
        total_grams_converted += capacity
    elif choice == 2:
        print ("Choose a model....")
        for machine in machines:
            print ("{} {} machines".format(capacity / machine.cost, machine.name))
    elif choice == 3:
        pass

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

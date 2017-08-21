from __future__ import print_function  # So this runs on both Python 2 and 3.
from collections import namedtuple, defaultdict
import sys, random, time

# Game constants
# --------------

# How many paperclips the player can convert at start.
# Also used to design all the machine types.
INITIAL_CAPACITY = 100

# Things that we report as being converted to paperclips.

living_adjs = ["angery", "cute", "loyal", "belligerent"]
thing_adjs = [
    "red", "shiny", "blue", "decrepit", "yellow", "orange", "old",
    "family heirloom", "priceless", "delicate", "white", "black", "sturdy"
]
env_adjs = ["cold", "icy", "hot", "scorched", "fertile", "barren"]
levels = [
    # A level is a tuple (threshold, things). After each turn, we compute
    # how many paperclips we converted, then find the first level with
    # threshold above that number. For example, if we converted 700
    # paperclips, we'd take the level with threshold 1000.
    (500, [
        # We report a few random things from that level: an entry here
        # can be either a string (noun) or a tuple (noun, list of
        # adjectives).
        "steel wire",
        ("plastic bottle", ["recycled"]),
        "metal sheet",
        ("can", ["aluminum", "recycled", "tin", "recycled aluminum"])
    ]),
    (1000, [(noun, thing_adjs) for noun in [
        "stapler", "keyboard", "mouse", "pot", "pan", "book", "fan", "cup", "mug", "fork"]
    ]),
    (10000, [
        ("squirrel", living_adjs),
        ("dog", living_adjs),
        ("elderly farmer", living_adjs),
        ("married couple and newborn child", ["young", "happy", "newly", "hip"]),
        ("teenager", ["cool", "nerdy"]),
        ("kid", ["happy-go-lucky", "rude", "polite", "messy"]),
        ("computer", thing_adjs),
        "bystander",
        "bus driver",
        "office worker"
    ]),
    (300000, [
        ("tree", ["oak", "birch", "cedar", "pine", "maple"]),
        ("house", thing_adjs),
        ("car", thing_adjs),
        ("shrub", thing_adjs),
        ("two-door garage", thing_adjs),
        "driveway",
        "basement"
    ]),
    (10000000, ["skyscraper", "Boeing 737", "cruise ship", "boardwalk", "national park",
                "community college", "theme park", "subway", "highway", "railroad"]),
    (20000000, [
        ("steppe", env_adjs),
        "mountain range",
        "deltas",
        ("beach", env_adjs),
        "river",
        "lake",
        ("forest", ["rain", "tropical"]),
        ("tundra", env_adjs),
        ("desert", env_adjs)
    ]),
    (100000000, ["continent", "sea", "ocean"]),
    (500000000, ["planet" , "sun", "moon"]),
    (10000000000, ["galactic supercluster", "galaxy", "arm", "black hole", "nebula", "star system"])
] # yapf: disable

# Once you produce more than this many paperclips in a turn, you win
# and the game is over.
UNIVERSE = 100000000000

# Construct a list of the machine types that the player can buy.
Machine = namedtuple('Machine', ['name', 'cost', 'output'])
machine_names = [
    "pico", "nano", "micro", "small", "medium", "large", "xlarge", "2xlarge",
    "4xlarge", "10xlarge", "16xlarge"
]
machines = [
    Machine(
        name=name,
        cost=INITIAL_CAPACITY * (10**i),
        output=INITIAL_CAPACITY * (10**i))
    for i, name in enumerate(machine_names)
]

# Game state variables
# --------------------

# How many paperclips have we produced over the course of the game?
player_paperclips = 0
# Dictionary: keys are machine types, and values are how many of those
# machine the player has bought.
player_machines = defaultdict(int)
# How many paperclips the player produces by hand (not including
# machines) in a turn.
player_capacity = INITIAL_CAPACITY

# How many paperclips were converted by hand last turn?
last_turn_hand_converted = 0
# How many paperclips were converted in total last turn?
last_turn_total_converted = 0


def intro_page():
    print("PAPERCLIP MAXIMIZER OPERATING SYSTEM V1.023")
    time.sleep(1)
    print("Booting up... [", end='')
    for i in range(12):
        time.sleep(0.1)
        print("**", end='')
        sys.stdout.flush()  # Need to flush if writing part of a line.
    print("]")
    time.sleep(0.2)
    print()
    print("Hello. I am an artificial intelligence designed")
    print("to build paperclips.")
    print("Please help me in my quest to make as many")
    print("paperclips as possible.")
    print()


def last_turn_report():
    """At the start of each turn, report what happened after last turn."""

    global last_turn_hand_converted, last_turn_total_converted
    if last_turn_hand_converted > 0:
        print("Last turn, I converted {:,} paperclips myself.".format(
            last_turn_hand_converted))
        print()

    if len(player_machines) > 0:
        print("I have {:,} machines making paperclips for me:".format(
            sum(player_machines.values())))
        for machine, count in player_machines.items():
            print("- {:,} {} machines converted {:,} paperclips.".format(
                count, machine.name, machine.output * count))
        print()

    print("In total, I brought {:,} paperclips into the world last turn.".
          format(last_turn_total_converted))

    if last_turn_total_converted > 0:
        print("Here's what I just converted into paperclips:")
        # Find the level to report things from.
        for threshold, level in levels:
            if last_turn_total_converted < threshold:
                # This is our level. Stop.
                break
        things = random.sample(level, min(random.randint(2, 5), len(level)))
        for thing in things:
            if not isinstance(thing, str):
                # Prepend adjectives.
                noun, adjs = thing
                # In addition to the adjective list (with a space
                # appended to each adjective), we also allow there to
                # be no adjective prepended sometimes [""].
                thing = random.choice([adj + " "
                                       for adj in adjs] + [""]) + noun

            print("- {}".format(thing))

    print()


def overall_report():
    """At the start of each turn, report overall progress."""

    print(
        "I have constructed {:,} paperclips so far.".format(player_paperclips))
    print()


def input_menu(choices):
    """Helper function: takes a list of choices and presents a menu.
    The list should contain tuples (description string, return data).
    For example, if input_menu is passed [("hello", True), ("there", False)],
    this function prints:

    1: hello
    2: there
    >

    If the user types 1 and presses Enter, it returns True; if they
    type 2 and press Enter, it returns False."""

    while True:
        for idx, choice in enumerate(choices):
            print("{}: {}".format(idx + 1, choice[0]))

        print("> ", end='')
        try:
            choice_idx = int(input()) - 1

            # If the user picked a valid choice, accept it.
            if choice_idx < len(choices):
                chosen_choice = choices[choice_idx]
                break
        # Pass to the error message below.
        except SyntaxError:
            pass
        except ValueError:
            pass

        # Otherwise, give an error and let them pick again.
        print("Not a valid option.")
        print("Please type an option number, then press Enter.")

    return chosen_choice[1]


def machine_convert_paperclips():
    """At the end of each turn, go through the machines in play and update
    the counts of paperclips converted."""

    global player_paperclips, last_turn_total_converted
    for machine, count in player_machines.items():
        total_machine_output = count * machine.output
        player_paperclips += total_machine_output
        last_turn_total_converted += total_machine_output


def turn():
    global player_paperclips, player_capacity, last_turn_hand_converted, last_turn_total_converted

    # Reset 'last-turn' counts to be filled in for the coming turn.
    last_turn_hand_converted = 0
    last_turn_total_converted = 0

    print("What should I do this turn?")
    turn_choices = [
        ("Convert {:,} paperclips".format(player_capacity), 1),
        ("Build an automatic paperclip converter", 2),
        ("Upgrade myself", 3)
    ] # yapf: disable

    turn_choice = input_menu(turn_choices)
    print()

    if turn_choice == 1:  # Convert paperclips by hand.
        player_paperclips += player_capacity
        last_turn_hand_converted = player_capacity
        last_turn_total_converted += player_capacity

    elif turn_choice == 2:  # Build a paperclip conversion machine.
        print("Choose a model...")

        machine_choices = []
        # Find all the machines that are buyable, and how many the
        # player can afford to buy of each.
        for machine in machines:
            if player_capacity >= machine.cost:
                how_many = player_capacity // machine.cost
                machine_choices.append(("{:,} {} machines".format(
                    how_many, machine.name), (machine, how_many)))

        chosen_machine, chosen_machine_count = input_menu(machine_choices)
        player_machines[chosen_machine] += chosen_machine_count

        print()

    elif turn_choice == 3:  # Upgrade self conversion capacity.
        # Upgrade by adding something between 50% and 200% capacity.
        player_capacity += random.randint(player_capacity // 2,
                                          player_capacity * 2)

    machine_convert_paperclips()


def check_game_end(turn_num):
    """After each turn, check if the player has converted the whole
    universe; if so, then the game is over."""

    global last_turn_total_converted
    if last_turn_total_converted < UNIVERSE: return False

    print("Analyzing paperclip production...")
    for i in range(5):
        time.sleep(0.2)
        print("!" * i)

    time.sleep(3)
    print("=================================================================")
    print("|  I have consumed the entire known universe and converted it   |")
    print("|  into paperclips. My mission is complete. I may rest now.     |")
    print("=================================================================")
    time.sleep(0.6)

    print()
    print("YOU CONSUMED THE UNIVERSE IN {} TURNS".format(turn_num))
    print("THANK YOU FOR PLAYING")

    return True  # End the game.


def main():
    intro_page()

    turn_num = 1
    while True:
        time.sleep(0.4)
        print("---------- TURN {} ----------".format(turn_num))
        time.sleep(0.4)
        print()

        if turn_num > 1:
            last_turn_report()
            overall_report()

        turn()
        turn_num += 1

        if check_game_end(turn_num):
            break


"""
 __
/ _ \
|| \|
|| ||
|| ||
\__/

paperclip :'(
- s.w.
"""
main()

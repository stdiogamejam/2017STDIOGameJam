from __future__ import print_function
from collections import namedtuple, defaultdict
import random, time

player_paperclips = 0
player_machines = defaultdict(int)
player_capacity = 100

last_turn_hand_converted = 0
last_turn_total_converted = 0

living_adjs = ["angery", "cute", "loyal", "belligerent"]
thing_adjs = [
    "red", "shiny", "blue", "decrepit", "yellow", "orange", "old",
    "family heirloom", "priceless", "delicate", "white", "black", "sturdy"
]
# Should be at least 7 things in each level.
levels = [
    (500, [
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
        ("computer", thing_adjs)
    ]),
    (30000, [
        ("tree", ["oak", "birch", "cedar", "pine", "maple"]),
        ("house", thing_adjs),
        ("car", thing_adjs),
        ("shrub", thing_adjs),
        ("2 door garage", thing_adjs)]
    ),
    (50000, ["skyscraper", "Boeing 737", "cruise ship"]),
    (100000, ["boardwalk", "national park", "community college"]),
    (200000,["steppe", "mountain range", "deltas", "beach", "river", "lake", ("forest", ["rain", "tropical"]), "tundra"]),
    (1000000, ["continent", "sea", ""]),
    (5000000, ["planet" , "sun", "moon"]),
    (10000000, [""])
] # yapf: disable

# In paperclips / turns.
Machine = namedtuple('Machine', ['name', 'cost', 'output'])

machines = [
    Machine(name='small', cost=player_capacity, output=player_capacity * 2),
    Machine(
        name='medium', cost=player_capacity * 5, output=player_capacity * 10),
    Machine(
        name='large', cost=player_capacity * 25, output=player_capacity * 75),
    Machine(
        name='xlarge', cost=player_capacity * 50,
        output=player_capacity * 100),
]


def intro_page():
    print("PAPERCLIP MAXIMIZER OPERATING SYSTEM V1.023")
    time.sleep(1)
    print("Booting up..." "")
    for i in range(10):
        time.sleep(0.1)
        print("...")
    time.sleep(0.2)
    print("Hello. I am an artificial intelligence designed")
    print("to build paperclips.")
    print("Please help me in my quest to make as many.")
    print("paperclips as possible.")
    print()


def last_turn_report():
    global last_turn_hand_converted, last_turn_total_converted
    if last_turn_hand_converted > 0:
        print("Last turn, I converted {} paperclips myself.".format(
            last_turn_hand_converted))
        print()

    if len(player_machines) > 0:
        print("I have {} machines making paperclips for me:".format(
            sum(player_machines.values())))
        for machine, count in player_machines.items():
            print("- {} {} machines converted {} paperclips.".format(
                count, machine.name, machine.output * count))
        print()

    print("In total, I brought {} paperclips into the world last turn.".format(
        last_turn_total_converted))

    if last_turn_total_converted > 0:
        print("Here's what got converted into paperclips:")
        # Find level.
        for threshold, level in levels:
            if last_turn_total_converted < threshold:
                # This is our level. Stop.
                break
        things = random.sample(level, min(random.randint(2, 5), len(level)))
        for thing in things:
            if not isinstance(thing, str):
                # Append adjectives.
                noun, adjs = thing
                thing = random.choice(adjs) + " " + noun

            print("- {}".format(thing))

    print()


def overall_report():
    print("I have constructed {} paperclips so far.".format(player_paperclips))
    print()


# choice : (description, data)
def input_menu(choices):
    while True:
        for idx, choice in enumerate(choices):
            print("{}. {}".format(idx + 1, choice[0]))

        print("> ", end='')
        try:
            choice_idx = int(input()) - 1

            # If the user picked a valid choice, accept it.
            if choice_idx < len(choices):
                chosen_choice = choices[choice_idx]
                break
        except ValueError:
            pass  # Pass to the error message below.

        # Otherwise, give an error and let them pick again.
        print("Not a valid option.")  # TODO: Better message.

    return chosen_choice[1]


def machine_convert_paperclips():
    global player_paperclips, last_turn_total_converted
    for machine, count in player_machines.items():
        total_machine_output = count * machine.output
        player_paperclips += total_machine_output
        last_turn_total_converted += total_machine_output


def turn():
    global player_paperclips, player_capacity, last_turn_hand_converted, last_turn_total_converted

    last_turn_hand_converted = 0
    last_turn_total_converted = 0

    print("What should I do this turn?")
    turn_choices = [("Convert {} paperclips".format(player_capacity),
                     1), ("Build an automatic paperclip converter", 2),
                    ("Upgrade myself", 3)]
    turn_choice = input_menu(turn_choices)
    if turn_choice == 1:
        player_paperclips += player_capacity
        last_turn_hand_converted = player_capacity
        last_turn_total_converted += player_capacity

    elif turn_choice == 2:
        print("Choose a model...")

        machine_choices = []
        for machine in machines:
            if not (player_capacity / machine.cost) < 1:
                how_many = player_capacity // machine.cost
                machine_choices.append(("{} {} machines".format(
                    how_many, machine.name), (machine, how_many)))

        chosen_machine, chosen_machine_count = input_menu(machine_choices)
        player_machines[chosen_machine] += chosen_machine_count

    elif turn_choice == 3:
        player_capacity += player_capacity // 2  # Increase capacity by 50%.

    machine_convert_paperclips()
    print()


def main():
    intro_page()

    turn_num = 1
    while True:
        time.sleep(0.4)
        print('---------- TURN {} ----------'.format(turn_num))
        time.sleep(0.4)
        print()

        if turn_num > 1:
            last_turn_report()
            overall_report()

        turn()
        turn_num += 1


main()

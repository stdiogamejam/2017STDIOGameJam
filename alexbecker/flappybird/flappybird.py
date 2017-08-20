#! /usr/bin/python3
# Copyright (c) Alex Becker 2017
# Licensed under the MIT license, available at https://opensource.org/licenses/MIT
import shutil
import random
import sys

# Cheats.
noclip = 'noclip' in sys.argv
nomove = 'nomove' in sys.argv

columns, lines = shutil.get_terminal_size()
height = lines - 1    # b/c the prompt takes up one line

banner = """
Welcome to turn-based flappy bird!

Each turn, press 'y' and hit enter to flap,
or just hit enter to let gravity do its thing.
Flapping will accelerate you upward, while
gravity will accelerate you downward.
Fly though as many gates as you can!

Remember conservation of momentum!
"""
print(banner)
for _ in range(lines - 1 - len(banner.split('\n'))):
    print()
input("Press enter to begin.")

# Start with the bird in the middle of the screen
bird_y = lines // 2
bird_velocity = 0

# Gates are either None if absent or a pair (y_min, y_max) indicating the opening.
# Start with one gate in the middle of the far right edge.
gates = [None] * (columns - 1)
last_gate = (lines // 2 - 2, lines // 2 + 2)
gates.append(last_gate)

turn = 0
playing = True
while playing:
    turn += 1

    # Print game state.
    for y in range(height):
        line = ''
        for x in range(columns):
            in_wall = False
            if gates[x]:
                low_end, high_end = gates[x]
                in_wall = low_end > y or high_end < y

            if x == columns // 2 and y == bird_y:
                if in_wall and not noclip:
                    playing = False
                line += '*'
            else:
                line += '|' if in_wall else ' '

        print(line)

    if not playing:
        break

    # Since y=0 is the top, flapping accelerates in the negative y direction.
    flap = input("Flap? [y/N]")
    if flap == 'y':
        bird_velocity -= 1
    else:
        bird_velocity += 1

    if not nomove:
        bird_y += bird_velocity
    if bird_y >= height or bird_y < 0:
        playing = False

    # Remove leftmost gate and add a new gate on the right.
    gates.pop(0)
    new_gate = None
    if turn % 4 == 0:
        # Every 4th turn, make a new gate shifted from the last gate by up to 3.
        gate_low, gate_high = last_gate
        # Make sure the delta doesn't shift the gate off screen.
        min_delta = max(-3, -gate_low)
        max_delta = min(3, height - 1 - gate_high)
        delta = random.randint(min_delta, max_delta)
        new_gate = (gate_low + delta, gate_high + delta)
        last_gate = new_gate
    gates.append(new_gate)

print("Game over! Score: %d" % turn)

"""Game entry for stdio jam"""
from __future__ import print_function

import json
from operator import itemgetter
import random
import sys


def header_print(output):
    """A pretty header print"""
    print("\n----------------------------------------------------------------")
    print(output)
    print("----------------------------------------------------------------")


def card_format(card):
    """A pretty and standard way to display cards"""
    pretty_output = '%s pts: %d  powers: %s' % (
        card['name'],
        card['points'],
        ', '.join(card['powers'])
    )
    pretty_output += ' desc: %s' % card['description']
    return pretty_output


class TinkerGame(object):
    """Class to run the game"""
    stats = {}

    def __init__(self):
        """open the data file and read it all into self.data"""
        with open('data.json') as data_file:
            self.data = json.load(data_file)
            self.game_over = False

    def setup(self):
        """Set up the hand, shuffle the deck, give initial powers"""
        header_print(self.data['intro'])
        header_print(self.data['help'])
        random.shuffle(self.data['draw'])
        random.shuffle(self.data['locations'])
        random.shuffle(self.data['events'])
        random.shuffle(self.data['aces'])
        random.shuffle(self.data['personalities'])
        self.stats = {
            'round': 0,
            'powers': {
                'MOONS': 6,
                'SUNS': 6,
                'WAVES': 6,
                'LEAVES': 6,
                'WYRMS': 6,
                'KNOTS': 6,
            },
            'hand': self.data['draw'][:],
            'discard': [],
            'active': [],
            'opponent': {},
        }

    def present_status(self):
        """Display the user's current status"""
        output = ''
        if self.stats['hand']:
            output += 'Ready: \n'
            for card in sorted(self.stats['hand'], key=itemgetter('name')):
                output += card_format(card) + '\n'
            output += '\n'
        if self.stats['active']:
            output += 'Active: \n'
            for card in self.stats['active']:
                output += card_format(card) + '\n'
        if self.stats['discard']:
            output += '\nSpent: \n'
            for card in self.stats['discard']:
                output += card_format(card) + '\n'
            output += '\n'
        output += 'Spells: \n'
        for power in self.stats['powers']:
            output += '%s x %d\n' % (power, self.stats['powers'][power])
        if self.stats['opponent']:
            output += '\nCurrent Activity:\n'
            output += '%s' % (card_format(self.stats['opponent']))
        header_print('Status')
        print(output)

    def present_menu(self, options, title='Menu:'):
        """Generic menu presentation returns index of options"""
        output = ''
        for count, option in enumerate(options):
            output += '%d) %s\n' % (count+1, option)
        output += '\nh) Help\ns) Status\nq) Quit\n'
        user_input = 0
        while user_input <= 0 or user_input > len(options):
            header_print(title)
            print(output)
            print(
                "Select an option from above (1-%d, h, s, or q):" % len(
                    options
                ),
                end=''
            )
            user_input = raw_input()
            if user_input.isdigit():
                user_input = int(user_input)
            elif user_input == 'h':
                header_print(self.data['help'])
            elif user_input == 's':
                self.present_status()
            elif user_input == 'q':
                sys.exit()
            else:
                print("Not a valid option")
        return user_input - 1

    def calculate_points(self):
        """add up the points from the user's stats"""
        points = 0
        for power in self.stats['powers']:
            points += self.stats['powers'][power]
        return points

    def play(self):
        """This checks and sets which round you're playing"""
        if self.stats['round'] == 0:
            if self.data['personalities'] and self.data['events']:
                self.choose_opponent()
                self.resolve_conflict()
            else:
                self.stats['round'] += 1
        elif self.stats['round'] == 1:
            if self.data['locations']:
                self.choose_location()
                self.resolve_conflict()
            else:
                self.stats['round'] += 1
        else:
            print("You've won")
            self.game_over = True
        return self.stats

    def choose_opponent(self):
        """Let the user choose an opponent"""
        possible_opponents = [
            self.data['personalities'].pop(),
            self.data['events'].pop()
        ]
        title = 'Recruit a member or gain experience:'
        options = []
        for possible_opponent in possible_opponents:
            option = card_format(possible_opponent)
            options.append(option)
        choice = self.present_menu(options, title)
        self.stats['opponent'] = possible_opponents[choice]

    def choose_location(self):
        """Automatically set the next location"""
        location = self.data['locations'].pop()
        self.stats['opponent'] = location

    def refresh_hand(self):
        """Add an amulet and reload hand from the discard pile"""
        if not self.stats['hand'] and self.stats['discard']:
            header_print('Adding a magic amulet and refreshing your group')
            if self.data['aces']:
                self.stats['discard'].append(self.data['aces'].pop())
            self.stats['hand'] = self.stats['discard'][:]
            self.stats['discard'] = []
            random.shuffle(self.stats['hand'])

    def display_current_situation(self, magic):
        """Display the active cards, the opponent, and relavant info"""
        usable_points = 0
        active_powers = []
        header_print("Your side of the struggle:")
        for card in self.stats['active']:
            print(card_format(card))
            for power in card['powers']:
                active_powers.append(power)
            for power in card['powers']:
                if power in self.stats['opponent']['powers']:
                    usable_points += card['points']
                    break
        print(
            "\nRelevant strength: %d   Magic: %d   Relevant powers: %s" % (
                usable_points,
                magic,
                ', '.join(
                    set(
                        self.stats['opponent']['powers']
                    ).intersection(active_powers)
                )
            )
        )
        header_print("The other side of the struggle:")
        print(card_format(self.stats['opponent']))
        return usable_points

    def resolve_conflict(self):
        """Resolve this conflict"""
        self.refresh_hand()
        self.stats['active'] = [self.stats['hand'].pop()]
        resolved = False
        magic = 0
        # while the conflict is not resolved
        while not resolved:
            self.refresh_hand()
            usable_points = self.display_current_situation(magic)
            # Check to see if we've defeated the opponent
            if usable_points + magic >= self.stats['opponent']['points']:
                # You beat your opponent
                if self.stats['round'] == 0:
                    header_print(
                        "Huzzah, you've gained %s" % (
                            self.stats['opponent']['name']
                        )
                    )
                    # if you defeat the opponent in round 1 you get the card
                    self.stats['discard'].append(self.stats['opponent'])
                elif self.stats['round'] == 1:
                    header_print(
                        "Huzzah, you've freed %s from evil" % (
                            self.stats['opponent']['name']
                        )
                    )
                self.stats['opponent'] = None
                resolved = True
            elif self.calculate_points() <= 0:
                header_print('You have failed in your quest')
                resolved = True
            else:
                # You haven't won, fled, or lost so present your options
                # and act on whatever you say to do
                title = 'Choose your next action: '
                options = []
                options.append('use a spell')
                if self.stats['round'] == 0:
                    options.append('flee')
                action = self.present_menu(options, title)
                if action == 1 and self.stats['round'] == 0:
                    header_print(
                        'You run away from %s' % self.stats['opponent']['name']
                    )
                    resolved = True
                elif action == 0:
                    if not self.stats['hand']:
                        header_print(
                            'You could not overcome %s' % (
                                self.stats['opponent']['name']
                            )
                        )
                        self.stats['active'] = []
                        resolved = True
                    else:
                        magic = self.cast_spell(magic)
        for card in self.stats['active']:
            self.stats['discard'].append(card)
        self.stats['active'] = []

    def cast_spell(self, magic):
        """Use one point from your powers dict to play a card from your hand"""
        title = 'Select type of spell to cast'
        options = self.stats['powers'].keys()
        option_display = []
        for power in options:
            option_display.append(
                "%s x %d" % (
                    power,
                    self.stats['powers'][power]
                )
            )
        choice = self.present_menu(option_display, title)
        self.stats['powers'][options[choice]] -= 1
        if self.stats['powers'][options[choice]] == 0:
            self.stats['powers'].pop(options[choice], None)
        if options[choice] in self.stats['opponent']['powers']:
            print(
                'A %s spell increases your magic during this trial' % (
                    options[choice]
                )
            )
            magic += 1
        print('Casting a spell...')
        self.stats['active'].append(self.stats['hand'].pop())
        return magic

    def end(self):
        """End the game"""
        self.present_status()
        header_print("GAME OVER")


def main():
    """The main python method"""
    game = TinkerGame()
    game.setup()
    while game.calculate_points() > 0 and not game.game_over:
        game.play()
    game.end()


main()

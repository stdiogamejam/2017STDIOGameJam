#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Goat <goat@ridiculousglitch.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
from string import Template
from time import time, sleep
import re, json, random

try:
    # Try to load fonts file from current directory
    with open('fonts.json', 'r') as f:
        FONTS = json.load(f)
except:
    FONTS = {}

def text_render(text, font_name=None):
    try:
        font = FONTS[font_name]
        return '\n'.join([ ''.join([ font['graphics'][ord(c)][i] for c in text ]) for i in range(font['height']) ])
    except KeyError:
        return text

def flushed_input(prompt=''):
    """Input function that flush the input buffer before reading, with optional prompt."""

    # Flush standard input before reading next string
    # Portable snippet from https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    # Read utf-8 input (try branch is for Python 2, except is for Python 3)
    try:
        return raw_input(prompt).decode('utf-8')
    except NameError:
        return input(prompt)

class Item(object):
    """Enumeration class."""

    MEDIKIT = 1
    AMMOS   = 2
    DOOR    = 3
    ZOMBIE  = 4

class Status(Template):
    """Status of the game.

    Implements status variables and update function. Also extends standard
    strings Template in order to expand status variables into template strings.
    """

    idpattern = r'([a-z][_a-z0-9]*)(\([0-9 ]*\))?'

    def __init__(self, initial_level=9, initial_health=5, initial_ammos=3):
        Template.__init__(self, '')
        self.level = initial_level
        self.health = initial_health
        self.ammos = initial_ammos
        self.score = 0

    @property
    def health_message(self):
        return u'{:<5}'.format(u'\xb7'*self.health)

    @property
    def ammos_message(self):
        return u'{:<5}'.format(u'\xb7'*self.ammos)

    @property
    def level_message(self):
        return u'{:^3}'.format(u'%s' % (self.level,) if self.level > 0 else u'G')

    def vspace(self, n=1):
        return '\n'*n

    def hspace(self, n=1):
        return ' '*n

    def get_random_item(self):
        d, w = random.random(), (1. + 9. / 20. - self.level / 20.)
        if d <= 0.15 * w:
            return Item.MEDIKIT
        elif d <= 0.3 * w:
            return Item.AMMOS
        elif d <= 0.5 * w:
            return Item.DOOR
        return Item.ZOMBIE

    def update(self, item):
        """Update game status and return result."""

        result = None
        if self.health > 0:
            if item == Item.MEDIKIT:
                if self.health < 5:
                    self.health += 1
                    result = '* You found a Medikit: +1 Health'
                else:
                    result = '* You found a Medikit: Health at maximum'
            elif item == Item.AMMOS:
                if self.ammos < 5:
                    self.ammos += 1
                    result = '* You found ammunitions: +1 Ammo'
                else:
                    result = '* You found: Ammo at maximum'
            elif item == Item.ZOMBIE:
                if self.ammos > 0:
                    self.ammos -= 1
                    result = '* You shoot to the zombie: -1 Ammo'
                else:
                    self.health -= 1
                    result = '* The zombie hit you %s' % ('but you kill him with your bare hands: -1 Health' if self.health > 0 else 'and you died',)
                self.score += 1 if self.health > 0 else 0
        return result

    def expand(self, template):
        """String template expansion, accepting function calls.

        Template variables come from the object attributes. Functions must have
        zero or more *integer* parameters, e.g.:
            $foo()
            ${bar(42)}
            ${zoe(1 2 3)}
        """

        self.template = template
        return self.safe_substitute(self)

    def print_passage(self, p):
        """Passage print method.

        A passage is a multiline text to be printed marking a rhythm. In other
        words, a passage is a list of lines moving forward at a certain speed.
        Technically a passage is a dictionary:
            { 'text': <str>, 'vel': <float>, 'accel': <float>, 'font': <str> }
        where all the keys are optional. The text (if any) is first expanded
        with status variables, then rendered with the specified font (if present)
        and finally written to standard output, using "vel" [ line/s ] and
        "accel" [ line/s^2 ].
        """

        vel = p.get('vel', 0)      # Passage velocity in line/s
        accel = p.get('accel', 0)  # Passage acceleration in line/s^2

        # Expand status variables in text and iterate line by line
        for line in text_render(self.expand(p.get('text', '')), p.get('font', None)).split('\n'):
            print(line)

            # Evaluate sleep time, which is the time between two lines
            # dt [s] = 1 [line] / vel [line/s] (if velocity is positive defined)
            dt = (1. / vel) if vel > 0 else 0
            sleep(dt)

            # Update velocity according to acceleration
            # vel [line/s] += dt [s] * accel [line/s^2]
            vel += dt * accel

    def print_passages(self, passages):
        """Print multiple passages."""

        for p in passages:
            self.print_passage(p)

    def __getitem__(self, key):
        """Redefine subscript operator for template substitutions."""

        # Split attribute name from (optional) call arguments
        attr_name, attr_args = re.match(Status.idpattern, key).groups()

        # Get attribute. If it's callable (attribute is an object method),
        # then call it with its arguments, if any.
        f = getattr(self, attr_name)
        if callable(f):
            f = f(*(map(int, attr_args.strip(' ()').split()) if attr_args is not None else []))
        return f

if __name__ == '__main__':
    # Init pseudorandom and load data
    random.seed()
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Main loop
    intro_begin = 0
    while True:
        # Create game status and print fancy intro
        status = Status(**data['setup'])
        status.print_passages(data['intro'][intro_begin:])
        intro_begin = 4

        # Game loop: repeat while alive and level is not ground
        while status.health > 0 and status.level > 0:
            # Print random amount of scrolling wall, then the door
            for _ in range(random.randint(4, 20)):
                status.print_passages(data['graphics']['wall'])
            status.print_passages(data['graphics']['door'])

            # Ask for action
            action = flushed_input('[E]nter/[d]own/e[x]it> ').lower()
            if action.startswith('d'):
                status.level -= sum([ x == 'd' for x in action ])
            elif action.startswith('x'):
                status.level = 0
            else:
                # If action is "Enter", extract three items
                items, doors_left = [ status.get_random_item() for _ in range(3) ], [ True ]*3
                while any(doors_left):
                    # Print items graphics using "symbols" font
                    status.print_passage({ 'text': text_render('\x05'.join(map(chr, items)), 'symbols'), 'vel': 12 })

                    # Check if there are doors to open and let the user choose what to do
                    j = 0
                    for i in range(3):
                        if items[i] != 3:
                            doors_left[i] = False
                        elif doors_left[i]:
                            if flushed_input('Open the %s door [Y/n]? ' % ('first' if j == 0 else ('second' if j == 1 else 'third'))).lower() != 'n':
                                items[i] = status.get_random_item()
                                break
                            else:
                                doors_left[i] = False
                            j += 1

                # Update status and report the results. Then go one level down
                status.print_passage({ 'text': '', 'vel': 1 })
                status.print_passage({ 'text': '\n'.join(filter(None, [ status.update(item) for item in items ])), 'vel': 1 })
                status.print_passage({ 'text': '', 'vel': 1 })
                status.level -= 1

        # Game over. Continue?
        status.print_passages(data['messages']['gameover_%s' % ('win' if status.health > 0 else 'lose',)])
        if flushed_input('Play again [Y/n]? ').lower() == 'n':
            break

    print('Thanks for playing!')

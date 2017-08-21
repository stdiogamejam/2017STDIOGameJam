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
from difflib import SequenceMatcher
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

class Status(Template):
    """Status of the game.

    Implements status variables and update function. Also extends standard
    strings Template in order to expand status variables into template strings.
    """

    idpattern = r'([a-z][_a-z0-9]*)(\([0-9 ]*\))?'

    def __init__(self, initial_time, underlined_ratio, initial_turn=1):
        Template.__init__(self, '')
        self._time_left = initial_time
        self.underlined_ratio = underlined_ratio
        self.turn = initial_turn
        self.sentence_len = self.bonus = self.total_score = self.time_taken = 0

    @property
    def time_left(self):
        return round(self._time_left, 1)

    @property
    def time_bonus(self):
        return max(0, round(self.bonus * (1. + self.sentence_len / 1000.) * 4., 1))

    @property
    def time_bonus_message(self):
        return 'Bonus %d points (+%.1fs)\n' % (self.score, self.time_bonus) if self.time_bonus > 0 else 'No bonus\n'

    @property
    def time_gain(self):
        return '%+.1fs' % (self.time_bonus - self.time_taken,)

    @property
    def score(self):
        return int(round(self.bonus * 100.))

    def vspace(self, n=1):
        return '\n'*n

    def hspace(self, n=1):
        return ' '*n

    def update(self, time_taken, sentence_len, bonus):
        """Update game status."""

        self.sentence_len = sentence_len
        self.bonus = bonus
        self.time_taken = time_taken
        self._time_left = max(0, self._time_left - self.time_taken + self.time_bonus)
        self.total_score += self.score
        self.turn += 1

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

def create_line_passages(sentence, words, line_first_word, line_last_word):
    """Create passages for line from line_first_word to line_last_word, with
    underlined words to type."""

    s, underline = words[line_first_word][0], ''
    for wstart, wend, wtype in words[line_first_word:line_last_word]:
        if wtype:
            underline += (' '*(wstart - s)) + (u'¯'*(wend - wstart))
            s = wend
    return [ { 'text': sentence[words[line_first_word][0]:words[line_last_word][0]] }, { 'text': underline, 'vel': 10 } ]

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

        # Game loop: continue while there's time left
        corpus = data['corpus']
        while status.time_left > 0:
            status.print_passages(data['messages']['turn'])

            # Search a sentence of length proportional to current turn no.
            sentence = None
            while sentence is None or len(sentence) < status.turn * 8 or len(sentence) > (status.turn + 5) * 8:
                sentence = corpus[random.randint(0, len(corpus) - 1)]['text']

            # Iterate over words (substrings in the sentence matching regex, that is,
            # starting with an alphanumeric and continuing with optionals
            # alphanumerics, hyphens or apostrophes). Construct a list of items:
            #   [ start_word_index, end_word_index, word_to_type (initially False) ]
            words = [ [ m.start(), m.end(), False ] for m in re.finditer(r'[a-zA-Z0-9]([a-zA-Z0-9\'-]*[a-zA-Z0-9])*', sentence, flags=re.I | re.U) if m.end() > m.start() ]

            # Select a random number of words and set word_to_type=True
            for word in random.sample(words, int(1 + status.underlined_ratio * len(words))):
                word[2] = True

            # Append a "fake" last item starting at the end of the sentence
            words.append([ len(sentence) - 1, 0, False ])

            # Create passages fitting a single 80-column line with underlined words
            passages, line_first_word = [], 0
            for line_last_word, (w2start, _, _) in enumerate(words[1:]):
                if w2start - words[line_first_word][0] >= 80:
                    passages.extend(create_line_passages(sentence, words, line_first_word, line_last_word))
                    line_first_word = line_last_word
            passages.extend(create_line_passages(sentence, words, line_first_word, line_last_word + 1))

            # Print created passages
            status.print_passages(passages)

            # Read input and time taken to digit
            time_taken = time()
            typed_words = flushed_input('> ')
            time_taken = round(time() - time_taken, 1)

            # Create a matcher object to evaluate the match ratio between underlined and actually typed words
            matcher = SequenceMatcher(a=typed_words.lower(), b=u' '.join([ sentence[w[0]:w[1]] for w in words if w[2] ]).lower())

            # Update the status and print turn report
            status.update(time_taken, len(sentence), matcher.ratio())
            status.print_passages(data['messages']['report'])

        # Game over. Continue?
        status.print_passages(data['messages']['gameover'])
        if flushed_input('Play again [Y/n]? ').lower() == 'n':
            break

    print('Thanks for playing!')

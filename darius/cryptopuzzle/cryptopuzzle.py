"""
Cryptogram puzzles.
"""

import itertools, string

def main():
    play_puzzle(get_cryptogram())

def get_cryptogram():
    print "Enter the encrypted puzzle, followed by a line with only a period ('.') to mark the end:"
    lines = []
    while True:
        line = raw_input()
        if line.strip() == '.': break
        lines.append(clean(line.lower()))
    return '\n'.join(lines)

def clean(s):
    "Expand tabs; blank out other control characters."
    r = ''
    for c in s:
        if c == '\t':
            while True:
                r += ' '
                if len(r) % 8 == 0: break
        elif ord(c) < 32:
            r += ' '
        else:
            r += c
    return r

alphabet = string.ascii_lowercase

def play_puzzle(cryptogram):
    code = ''.join(c for c in cryptogram if c.isalpha())
    if not code:
        print "No text to decrypt!"
        return
    decoder = {c: ' ' for c in set(code)}
    lines = cryptogram.splitlines()

    while True:
        used = set(decoder.values()) - set(' ')
        letters_left = ''.join(' ' if c in used else c for c in alphabet)

        for line in lines:
            print
            print ''.join(decoder.get(c, c) for c in line)
            print ''.join(' -'[c.isalpha()] for c in line)
            print line
        print
        print "Free: %s\n" % letters_left

        while True:
            command = raw_input("Enter a substitution like 'crypt/plain': ")
            if not command.strip():
                quitting = raw_input("Do you want to quit? ('y' for yes) ")
                if 'y' in quitting.lower():
                    return
            if '/' in command: break
            print "Enter something like 'abc/xyz', or just hit Enter if you want to quit."

        pattern, replacement = command.split('/', 2)
        for p, r in itertools.izip_longest(pattern, replacement, fillvalue=' '):
            if p.isalpha():
                decoder[p] = r

if __name__ == '__main__':
    main()

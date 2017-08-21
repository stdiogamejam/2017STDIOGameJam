"""
Cryptogram puzzles.
"""

import string

# The input function has different names in Python 2 and 3. Adapt to that:
try: input = raw_input
except NameError: pass

def main():
    play_puzzle(get_cryptogram())

def get_cryptogram():
    print("Enter the encrypted puzzle, followed by a line with only a period ('.') to mark the end:")
    lines = []
    while True:
        line = input()
        if line.strip() == '.': break
        lines.append(line.lower())
    return lines

alphabet = string.ascii_lowercase

def play_puzzle(lines):
    code = ''.join(c for line in lines for c in line if c.isalpha())
    if not code:
        print("No text to decrypt!")
        return
    decoder = {c: ' ' for c in set(code)}

    while True:
        used = set(decoder.values()) - set(' ')
        letters_left = ''.join(' ' if c in used else c for c in alphabet)

        for line in lines:
            print('')
            print(''.join(decoder.get(c, c) for c in line))
            print(''.join(' -'[c.isalpha()] for c in line))
            print(line)
        print('')
        print("Free: %s\n" % letters_left)

        while True:
            command = input("Enter a substitution like 'crypt/plain': ")
            if not command.strip():
                quitting = input("Do you want to quit? ('y' for yes) ")
                if 'y' in quitting.lower():
                    return
            if '/' in command: break
            print("Enter something like 'abc/xyz', or just hit Enter if you want to quit.")

        pattern, replacement = command.split('/', 2)
        for p, r in zip(pattern, replacement + ' '*len(pattern)):
            if p.isalpha():
                decoder[p] = r

if __name__ == '__main__':
    main()

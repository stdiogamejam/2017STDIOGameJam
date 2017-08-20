"""
Create a cryptogram from plaintext from either the command line or `fortune`.
"""

import commands, random, string, sys

def main(argv):
    if   len(argv) == 1: plaintext = fortune()
    elif len(argv) == 2: plaintext = argv[1]
    else:
        print("Usage: python %s [cryptogram]" % sys.argv[0])
        sys.exit(1)
    print(clean(random_encrypt(plaintext)))

alphabet = string.ascii_lowercase

def random_encrypt(text):
    values = list(alphabet)
    random.shuffle(values)
    code = dict(zip(alphabet, values))
    return ''.join(code.get(c, c) for c in text.lower())

def fortune():
    return shell_run('fortune')

def shell_run(command):
    err, output = commands.getstatusoutput(command)
    if err:
        print(output)
        sys.exit(1)
    return output

def clean(s):
    "Expand tabs; blank out other control characters."
    r = ''
    for c in s:
        if c == '\t':
            while True:
                r += ' '
                if len(r) % 8 == 0: break
        elif c == '\n' or 32 <= ord(c):
            r += c
        else:
            r += ' '
    return r

if __name__ == '__main__':
    main(sys.argv)

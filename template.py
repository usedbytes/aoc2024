import sys

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        print(line)

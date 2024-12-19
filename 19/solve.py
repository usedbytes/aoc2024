import sys

from functools import cache

@cache
def make_towel(towel, fragments):
    for f in fragments:
        if f == towel:
            return True
        elif towel.startswith(f):
            if make_towel(towel[len(f):], fragments):
                return True

    return False

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)

    fragments = tuple(next(lines).split(", "))

    p1 = 0
    for line in lines:
        if line == "":
            continue

        p1 += make_towel(line, fragments)
print(p1)

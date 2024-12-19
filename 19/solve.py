import sys

from functools import cache

@cache
def make_towel(towel, fragments):
    ways = 0
    for f in fragments:
        if f == towel:
            ways += 1
        elif towel.startswith(f):
            ways += make_towel(towel[len(f):], fragments)

    return ways

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)

    fragments = tuple(next(lines).split(", "))

    p1, p2 = 0, 0
    for line in lines:
        if line == "":
            continue

        ways = make_towel(line, fragments)
        if ways > 0:
            p1 += 1
        p2 += ways
print(p1)
print(p2)

import sys

from collections import defaultdict
from itertools import combinations

antennas = defaultdict(list)

with open(sys.argv[1]) as f:
    width = 0
    row = 0
    for line in map(str.strip, f):
        for col, char in enumerate(line):
            if char == ".":
                continue
            antennas[char].append((col, row))
        width = len(line)
        row += 1
    height = row

def in_bounds(an):
    if an[0] < 0 or an[1] < 0:
        return False

    if an[0] >= width or an[1] >= height:
        return False

    return True

antinodes = set()

for freq, ant in antennas.items():
    for pair in combinations(ant, 2):
        dr, dc = (pair[1][0] - pair[0][0]), (pair[1][1] - pair[0][1])

        an1 = (pair[0][0] - dr, pair[0][1] - dc)
        an2 = (pair[1][0] + dr, pair[1][1] + dc)

        if in_bounds(an1):
            antinodes.add(an1)
        if in_bounds(an2):
            antinodes.add(an2)

part1 = len(antinodes)
print(part1)

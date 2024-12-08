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
antinodes_p2 = set()

for freq, ant in antennas.items():
    for pair in combinations(ant, 2):
        dc, dr = (pair[1][0] - pair[0][0]), (pair[1][1] - pair[0][1])

        an1 = (pair[0][0] - dc, pair[0][1] - dr)
        an2 = (pair[1][0] + dc, pair[1][1] + dr)

        if in_bounds(an1):
            antinodes.add(an1)
        if in_bounds(an2):
            antinodes.add(an2)

        # Theres definitely two antennas in-line (they're a pair)
        # so they both count as part 2 antinodes
        antinodes_p2.add(pair[0])
        antinodes_p2.add(pair[1])

        while in_bounds(an1):
            antinodes_p2.add(an1)
            an1 = (an1[0] - dc, an1[1] - dr)

        while in_bounds(an2):
            antinodes_p2.add(an2)
            an2 = (an2[0] + dc, an2[1] + dr)

part1 = len(antinodes)
print(part1)

part2 = len(antinodes_p2)
print(part2)

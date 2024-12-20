import itertools
import sys

from collections import defaultdict

path_points = set()
with open(sys.argv[1]) as f:
    for y, line in enumerate(map(str.strip, f)):
        for x, char in enumerate(line):
            if char == ".":
                path_points.add((x, y))
            elif char == "S":
                start = (x, y)
                path_points.add(start)
            elif char == "E":
                end = (x, y)
                path_points.add(end)

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

# Build an ordered path
path = []
pos = start
while pos != end:
    path.append((pos[0], pos[1], len(path)))

    for d in dirs:
        npos = (pos[0] + d[0], pos[1] + d[1])
        if npos in path_points:
            if (
                len(path) >= 2 and
                (npos[0], npos[1]) == (path[-2][0], path[-2][1])
            ):
                # don't go back
                continue
            pos = npos
            break

assert pos == end
path.append((end[0], end[1], len(path)))

# Evaluate all path elements pairwise (use itertools.combinations)
# (around 45 million combinations)
# - If they're closer than 3 spaces
# - Not connected by path
#  ---> Possible cheat
# New path is then path[:cheat[0]] + path[cheat[1]:] 

# mapping from saved distance -> number of cheats
cheats = defaultdict(int)
for a, b in itertools.combinations(path, 2):
    if a[0] != b[0] and a[1] != b[1]:
        # can't cheat diagonally
        continue

    distance = abs(b[0] - a[0]) + abs(b[1] - a[1])
    if distance > 2:
        # too far to cheat
        continue

    start_idx = a[2]
    end_idx = b[2]
    new_length = start_idx + distance + (len(path) - end_idx)
    saved = len(path) - new_length
    if saved > 0:
        cheats[saved] += 1

p1 = 0
for k, v in cheats.items():
    if k >= 100:
        p1 += v
print(p1)

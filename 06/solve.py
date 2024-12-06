import sys

field = set()
with open(sys.argv[1]) as f:
    height = 0
    for y, line in enumerate(map(str.strip, f)):
        height += 1
        width = len(line)
        for x, v in enumerate(line):
            match v:
                case '#':
                    field.add((x, y))
                case '<':
                    start = (x, y)
                    move = (-1, 0)
                case '>':
                    start = (x, y)
                    move = (1, 0)
                case '^':
                    start = (x, y)
                    move = (0, -1)
                case 'v':
                    start = (x, y)
                    move = (0, 1)

turns = {
    (-1, 0): (0, -1),
    (1, 0): (0, 1),
    (0, -1): (1, 0),
    (0, 1): (-1, 0),
}

def simulate(start, move, field):
    guard = start
    visited = set()
    while True:
        if (guard, move) in visited:
            # Same place in same direction - we looped
            return set([v[0] for v in visited]), True

        visited.add((guard, move))
        new_pos = (guard[0] + move[0], guard[1] + move[1])
        if new_pos in field:
            # Would hit an obstacle
            move = turns[move]
        elif (
            new_pos[0] >= width or
            new_pos[1] >= height or
            new_pos[0] < 0 or
            new_pos[1] < 0
        ):
                break
        else:
            guard = new_pos

    return set([v[0] for v in visited]), False

part1, _ = simulate(start, move, field)
print(len(part1))

part2 = 0
# Brute-forcey but better than hitting every grid square. We only need to
# check places that the guard actually visited
for (x, y) in part1:
    if (x, y) in field:
        continue
    if (x, y) == start:
        continue
    new_field = field.copy()
    new_field.add((x, y))
    _, loop = simulate(start, move, new_field)
    if loop:
        part2 += 1
print(part2)

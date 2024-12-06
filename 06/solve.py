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
                    guard = (x, y)
                    move = (-1, 0)
                case '>':
                    guard = (x, y)
                    move = (1, 0)
                case '^':
                    guard = (x, y)
                    move = (0, -1)
                case 'v':
                    guard = (x, y)
                    move = (0, 1)

turns = {
    (-1, 0): (0, -1),
    (1, 0): (0, 1),
    (0, -1): (1, 0),
    (0, 1): (-1, 0),
}

visited = set()
while True:
    visited.add(guard)
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

part1 = len(visited)
print(part1)

import sys

grid = []
heads = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        line = [int(v) for v in line]
        for x, v in enumerate(line):
            if v == 0:
                heads.append((x, len(grid)))
        grid.append(line)

width = len(grid[0])
height = len(grid)

def walk_trail(grid, start, p2 = False):
    sx, sy = start
    start_height = grid[sy][sx]

    if start_height == 9:
        return 1 if p2 else set([start])

    dirs = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1],
    ]

    result = 0 if p2 else set()
    for d in dirs:
        nx, ny = sx + d[0], sy + d[1]
        if nx < 0 or nx >= width:
            continue
        if ny < 0 or ny >= height:
            continue
        next_height = grid[ny][nx]
        if next_height == start_height + 1:
            r = walk_trail(grid, (nx, ny), p2)
            if p2:
                result += r
            else:
                result.update(r)
    return result

p1 = 0
for head in heads:
    peaks = walk_trail(grid, head)
    p1 += len(peaks)
print(p1)

p2 = 0
for head in heads:
    p2 += walk_trail(grid, head, True)
print(p2)

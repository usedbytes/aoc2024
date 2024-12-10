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

def walk_trail(grid, start):
    sx, sy = start
    start_height = grid[sy][sx]

    if start_height == 9:
        return set([start])

    dirs = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1],
    ]

    result = set()
    for d in dirs:
        nx, ny = sx + d[0], sy + d[1]
        if nx < 0 or nx >= width:
            continue
        if ny < 0 or ny >= height:
            continue
        next_height = grid[ny][nx]
        if next_height == start_height + 1:
            result.update(walk_trail(grid, (nx, ny)))
    return result

p1 = 0
for head in heads:
    peaks = walk_trail(grid, head)
    p1 += len(peaks)
print(p1)

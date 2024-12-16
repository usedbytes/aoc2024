import heapq
import sys

grid = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        e = line.find("E")
        if e >= 0:
            end = (e, len(grid))

        s = line.find("S")
        if s >= 0:
            start = (s, len(grid))

        grid.append(line)

i = 0
q = []
directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

# q stores (cost, counter, pos, direction_idx)
# counter just ensures ordering, as mentioned in the docs
heapq.heappush(q, (0, i, start, 0))

# Stores minimum cost to reach (x, y, dir) - note that including the direction
# is important!
min_cost = {}

while q:
    cost, _, (x, y), cur_dir = heapq.heappop(q)
    if (x, y) == end:
        p1 = cost
        break

    for didx in range(len(directions)):
        dx, dy = directions[didx]
        nx, ny = x + dx, y + dy
        if grid[ny][nx] == "#":
            continue

        nturns = (didx - cur_dir) % 2
        new_cost = cost + (nturns * 1000) + 1

        if (nx, ny, didx) in min_cost:
            if min_cost[(nx, ny, didx)] <= new_cost:
                continue
        min_cost[(nx, ny, didx)] = new_cost

        i += 1
        heapq.heappush(q, (new_cost, i, (nx, ny), didx))

print(p1)

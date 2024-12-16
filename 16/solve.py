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

# q stores (cost, counter, pos, direction_idx, path)
# counter just ensures ordering, as mentioned in the docs
heapq.heappush(q, (0, i, start, 0, [start]))

# Stores minimum cost to reach (x, y, dir) - note that including the direction
# is important!
min_cost = {}

# Store all points on paths with the minimum cost
on_path = set()

p1 = None
while q:
    cost, _, (x, y), cur_dir, path = heapq.heappop(q)
    if (x, y) == end:
        if p1 == None or cost <= p1:
            p1 = cost
            on_path.update(path)
        # No need to break - we're only considering cheapest paths, so
        # the queue is only the "frontier", it won't grow out of hand.

    for didx in range(len(directions)):
        dx, dy = directions[didx]
        nx, ny = x + dx, y + dy
        if grid[ny][nx] == "#":
            continue

        nturns = (didx - cur_dir) % 2
        new_cost = cost + (nturns * 1000) + 1

        if (nx, ny, didx) in min_cost:
            if min_cost[(nx, ny, didx)] < new_cost:
                continue
        min_cost[(nx, ny, didx)] = new_cost

        new_path = path[:]
        new_path.append((nx, ny))

        i += 1
        heapq.heappush(q, (new_cost, i, (nx, ny), didx, new_path))

print(p1)

p2 = len(on_path)
print(p2)

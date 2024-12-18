import heapq
import sys

if sys.argv[1].endswith("input.txt"):
    width, height = 71, 71
    limit = 1024
else:
    width, height = 7, 7
    limit = 12
grid = [[0] * width for i in range(height)]

start = (0, 0)
end = (width - 1, height - 1)

def run_maze(grid):
    q = []
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]

    i = 0

    # q stores (cost, counter, pos)
    # counter just ensures ordering, as mentioned in the docs
    heapq.heappush(q, (0, i, start))

    # Stores minimum cost to reach (x, y)
    min_cost = {}

    while q:
        cost, _, (x, y) = heapq.heappop(q)
        if (x, y) == end:
            return cost

        for didx in range(len(directions)):
            dx, dy = directions[didx]
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx] == 1:
                # Can't move
                continue

            new_cost = cost + 1
            if (nx, ny) in min_cost:
                if min_cost[(nx, ny)] <= new_cost:
                    continue
            min_cost[(nx, ny)] = new_cost

            i += 1
            heapq.heappush(q, (new_cost, i, (nx, ny)))
    return None

with open(sys.argv[1]) as f:
    for i, line in enumerate(map(str.strip, f)):
        x, y = map(int, line.split(","))

        grid[y][x] = 1

        if i >= limit - 1:
            distance = run_maze(grid)
            if distance is None:
                # Part 2
                print(f"{x},{y}")
                break
            if i == limit - 1:
                # Part 1
                print(distance)

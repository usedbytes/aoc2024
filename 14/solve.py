import sys

width, height = 11, 7
if sys.argv[1].endswith("input.txt"):
    width, height = 101, 103

robots = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        ps, vs = line.split()
        sx, sy = map(int, ps[2:].split(","))
        vx, vy = map(int, vs[2:].split(","))

        robots.append(((sx, sy), (vx, vy)))

# Part 1, just simulate 100 steps
q = [0] * 4
for robot in robots:
    steps_to_sim = 100
    x, y = robot[0]
    vx, vy = robot[1]
    for _ in range(steps_to_sim):
        x = (x + vx) % width
        y = (y + vy) % height

    if x < width // 2:
        if y < height // 2:
            q[0] += 1
        if y > height // 2:
            q[3] += 1
    if x > width // 2:
        if y < height // 2:
            q[1] += 1
        if y > height // 2:
            q[2] += 1

print(q[0] * q[1] * q[2] * q[3])

# Part 2 - keep going until pattern repeats
positions = [r[0] for r in robots]
steps = 0
q = [0] * 4
while True:
    grid = [[0] * width for row in range(height)]
    stripes = [0] * 3

    for i, robot in enumerate(robots):
        x, y = positions[i]
        vx, vy = robot[1]
        x = (x + vx) % width
        y = (y + vy) % height
        positions[i] = (x, y)

        grid[y][x] += 1
        if x < width // 3:
            stripes[0] += 1
        elif x < width * 2 // 3:
            stripes[1] += 1
        else:
            stripes[2] += 1

    steps += 1
    if stripes[1] > stripes[0] + stripes[2]:
        # Print out the grid whenever the robots are centre-weighted. Seems a
        # good heuristic for finding picture-like things
        print("---")
        print(steps)
        for row in grid:
            s = "".join(map(lambda v: " " if v == 0 else str(v), row))
            print(s)
    if positions[0] == robots[0][0]:
        # Pattern repeats after ~10500 steps, all sequences are the same
        # length (for my input)
        break
print(steps)

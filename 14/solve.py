import sys

width, height = 11, 7
if sys.argv[1].endswith("input.txt"):
    width, height = 101, 103

with open(sys.argv[1]) as f:
    quadrants = [0] * 4
    for line in map(str.strip, f):
        ps, vs = line.split()
        sx, sy = map(int, ps[2:].split(","))
        vx, vy = map(int, vs[2:].split(","))

        steps_to_sim = 100
        x, y = sx, sy
        for _ in range(steps_to_sim):
            x = (x + vx) % width
            y = (y + vy) % height

        if x < width // 2:
            if y < height // 2:
                quadrants[0] += 1
            if y > height // 2:
                quadrants[3] += 1
        if x > width // 2:
            if y < height // 2:
                quadrants[1] += 1
            if y > height // 2:
                quadrants[2] += 1

print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])

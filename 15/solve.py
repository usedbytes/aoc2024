import sys

def shove(grid, start, direction):
    x, y = start
    dx, dy = direction
    nx, ny = x + dx, y + dy

    hit = grid[ny][nx]
    if hit == '.':
        this = grid[y][x]
        grid[ny][nx] = this
        grid[y][x] = '.'
        return direction
    elif hit == '#':
        return (0, 0)
    else:
        result = shove(grid, (nx, ny), direction)
        if result != (0, 0):
            this = grid[y][x]
            grid[ny][nx] = this
            grid[y][x] = '.'
        return result

grid = []
robot = None

move_dirs = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

def print_grid(grid):
    for row in grid:
        print("".join(row))

def calc_gps(grid):
    result = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "O":
                result += 100 * y + x
    return result

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)
    while True:
        line = next(lines)
        if len(line) == 0:
            # Map done
            break

        row = []
        for char in line:
            if char == "@":
                robot = (len(grid), len(row))
            row.append(char)
        grid.append(row)

    #print_grid(grid)
    try:
        while True:
            line = next(lines)
            for move in line:
                direction = move_dirs[move]
                rx, ry = shove(grid, robot, direction)
                robot = (robot[0] + rx, robot[1] + ry)
                #print_grid(grid)
    except StopIteration:
        pass

print(calc_gps(grid))

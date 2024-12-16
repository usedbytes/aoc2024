import sys

def shove(grid, start, direction, check_only = False):
    #print("shove", grid, start, direction, check_only)
    x, y = start
    dx, dy = direction
    nx, ny = x + dx, y + dy
    hit = grid[ny][nx]

    ok = False
    match hit:
        case ".":
            ok = True
        case "#":
            ok = False
        case "[":
            if dy == 0:
                # Moving horizontally, simple case
                ok = shove(grid, (nx, ny), direction, check_only)
            else:
                # Moving vertically, do both
                ok = (
                    shove(grid, (nx, ny), direction, check_only) and
                    shove(grid, (nx + 1, ny), direction, check_only)
                )
        case "]":
            if dy == 0:
                # Moving horizontally, simple case
                ok = shove(grid, (nx, ny), direction, check_only)
            else:
                # Moving vertically, do both
                ok = (
                    shove(grid, (nx - 1, ny), direction, check_only) and
                    shove(grid, (nx, ny), direction, check_only)
                )
        case _:
            ok = shove(grid, (nx, ny), direction, check_only)

    if ok and not check_only:
        this = grid[y][x]
        grid[ny][nx] = this
        grid[y][x] = '.'

    return ok

grid = []
robot = None

grid2 = []
robot2 = None

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
            if char == "O" or char == "[":
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
        row2 = []
        for char in line:
            match char:
                case "@":
                    robot = (len(row), len(grid))
                    robot2 = (len(row2), len(grid2))
                    row2.append("@")
                    row2.append(".")
                case "O":
                    row2.append("[")
                    row2.append("]")
                case _:
                    row2.append(char)
                    row2.append(char)
            row.append(char)
        grid.append(row)
        grid2.append(row2)

    moves = []
    try:
        while True:
            line = next(lines)
            for move in line:
                moves.append(move)
    except StopIteration:
        pass

for move in moves:
    direction = move_dirs[move]
    moved = shove(grid, robot, direction)
    if moved:
        robot = (robot[0] + direction[0], robot[1] + direction[1])
p1 = calc_gps(grid)
print(p1)

for move in moves:
    direction = move_dirs[move]

    # First check if everything is OK to move
    can_move = shove(grid2, robot2, direction, True)

    # Then do it
    if can_move:
        moved = shove(grid2, robot2, direction, False)
        assert moved
        robot2 = (robot2[0] + direction[0], robot2[1] + direction[1])
p2 = calc_gps(grid2)
print(p2)

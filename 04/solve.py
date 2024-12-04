import sys

grid = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        grid.append(line)

def search_from(r, c):
    dirs = [
        [1, 0],
        [1, 1],
        [0, 1],
        [-1, 1],
        [-1, 0],
        [-1, -1],
        [0, -1],
        [1, -1],
    ]

    num_found = 0
    for dc, dr in dirs:
        if (
            (dr < 0 and r < -dr * 3) or
            (dr > 0 and r >= len(grid) - dr * 3) or
            (dc < 0 and c < -dc * 3) or
            (dc > 0 and c >= len(grid[0]) - dc * 3)
        ):
            continue

        letters = (
            grid[r + dr][c + dc],
            grid[r + 2 * dr][c + 2 * dc],
            grid[r + 3 * dr][c + 3 * dc],
        )

        if letters == ("M", "A", "S"):
            num_found += 1
    return num_found

total = 0
for r, row in enumerate(grid):
    for c, letter in enumerate(row):
        if letter == "X":
            found = search_from(r, c)
            total += found
print(total)

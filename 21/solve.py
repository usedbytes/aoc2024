import enum
import sys
from functools import cache
from itertools import permutations, pairwise

# 789
# 456
# 123
# X0A
numpad_coords = {
    "X": (0, 0),
    "0": (1, 0),
    "A": (2, 0),
    "1": (0, 1),
    "2": (1, 1),
    "3": (2, 1),
    "4": (0, 2),
    "5": (1, 2),
    "6": (2, 2),
    "7": (0, 3),
    "8": (1, 3),
    "9": (2, 3),
}

# X^A
# <v>
dpad_coords = {
    "X": (0, 0),
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, -1),
    "v": (1, -1),
    ">": (2, -1),
}

directions = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, 1),
}

class PadType(enum.IntEnum):
    Number = 0
    Direction = 1

def build_numpad_graph():
    numpad_moves = {}
    for a, b in permutations(numpad_coords.items(), 2):
        ak, (ax, ay) = a
        bk, (bx, by) = b

        dx = bx - ax
        dy = by - ay

        xchar = ">" if dx > 0 else "<"
        ychar = "^" if dy > 0 else "v"

        move = xchar * abs(dx) + ychar * abs(dy)

        numpad_moves[(ak, bk)] = move

    for k, v in numpad_coords.items():
        numpad_moves[(k, k)] = ""
    
    return numpad_moves

def build_dpad_graph():
    dpad_moves = {}
    for a, b in permutations(dpad_coords.items(), 2):
        ak, (ax, ay) = a
        bk, (bx, by) = b

        dx = bx - ax
        dy = by - ay

        xchar = ">" if dx > 0 else "<"
        ychar = "^" if dy > 0 else "v"

        move =  xchar * abs(dx) + ychar * abs(dy)

        dpad_moves[(ak, bk)] = move

    for k, v in dpad_coords.items():
        dpad_moves[(k, k)] = ""

    return dpad_moves

def route_valid(a, route, coords):
    x = coords["X"]
    pos = coords[a]
    for char in route:
        dx, dy = directions[char]
        pos = (pos[0] + dx, pos[1] + dy)
        if pos == x:
            return False
    return True

@cache
def numpad_valid(a, route):
    return route_valid(a, route, numpad_coords)

@cache
def dpad_valid(a, route):
    return route_valid(a, route, dpad_coords)

def type_code(code, graph):
    # Starts at A
    code = "A" + code
    sequence = ""

    for pair in pairwise(code):
        sequence += graph[pair] + "A"

    return sequence

@cache
def shortest_sequence(code, pad_types):
    if len(pad_types) == 0:
        return len(code)

    pad_type = pad_types[0]
    graph = {
        PadType.Number: numpad_moves,
        PadType.Direction: dpad_moves,
    }[pad_type]

    valid = {
        PadType.Number: numpad_valid,
        PadType.Direction: dpad_valid,
    }[pad_type]

    result = 0
    for pair in pairwise("A" + code):
        canonical = graph[pair]
        min_len = None
        for perm in permutations(canonical):
            if not valid(pair[0], perm):
               continue
            new_len = shortest_sequence("".join(perm) + "A", pad_types[1:])
            if min_len is None or new_len < min_len:
                min_len = new_len
        result += min_len
    return result

numpad_moves = build_numpad_graph()
dpad_moves = build_dpad_graph()

codes = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        codes.append(line)

p1 = 0
pad_types = (PadType.Number, ) + 2 * (PadType.Direction, )
for code in codes:
    min_len = shortest_sequence(code, pad_types)
    complexity = int(code[:-1]) * min_len
    p1 += complexity
print(p1)

p2 = 0
pad_types = (PadType.Number, ) + 25 * (PadType.Direction, )
for code in codes:
    min_len = shortest_sequence(code, pad_types)
    complexity = int(code[:-1]) * min_len
    p2 += complexity
print(p2)

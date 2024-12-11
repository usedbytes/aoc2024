import functools
import math
import sys

with open(sys.argv[1]) as f:
    line = f.read().strip()
    stones = [int(v) for v in line.split()]

@functools.cache
def evaluate_stone(stone, nblinks):
    if nblinks == 0:
        return 1

    if stone == 0:
        return evaluate_stone(1, nblinks - 1)
    else:
        ndigits = len(str(stone))
        if ndigits % 2 == 0:
            bottom = stone % 10**(ndigits // 2)
            top = stone // 10**(ndigits // 2)

            a = evaluate_stone(top, nblinks - 1)
            b = evaluate_stone(bottom, nblinks - 1)
            return a + b
        else:
            return evaluate_stone(stone * 2024, nblinks - 1)

p1 = 0
p2 = 0
for stone in stones:
    p1 += evaluate_stone(stone, 25)
    p2 += evaluate_stone(stone, 75)

print(p1)
print(p2)

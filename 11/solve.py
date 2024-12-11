import math
import sys

with open(sys.argv[1]) as f:
    line = f.read().strip()
    stones = [int(v) for v in line.split()]
print(stones)

for blink in range(25):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        else:
            ndigits = len(str(stone))
            if ndigits % 2 == 0:
                bottom = stone % 10**(ndigits // 2)
                top = stone // 10**(ndigits // 2)
                new_stones.append(top)
                new_stones.append(bottom)
            else:
                new_stones.append(stone * 2024)
    stones = new_stones

print(len(stones))

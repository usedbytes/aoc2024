import sys

def is_safe(report):
    deltas = []
    for i, v in enumerate(report[1:]):
        deltas.append(v - report[i])

    return (
        (
            all(map(lambda v: v > 0, deltas)) or
            all(map(lambda v: v < 0, deltas))
        ) and (
            all(map(lambda v: 1 <= abs(v) <= 3, deltas))
        )
    )

part1 = 0

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        report = list(map(int, line.split()))

        if is_safe(report):
            part1 += 1

print(part1)

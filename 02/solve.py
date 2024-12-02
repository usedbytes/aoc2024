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

def is_dampened_safe(report):
    if is_safe(report):
        return True

    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True

    return False

part1 = 0
part2 = 0

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        report = list(map(int, line.split()))

        if is_safe(report):
            part1 += 1

        if is_dampened_safe(report):
            part2 += 1

print(part1)
print(part2)

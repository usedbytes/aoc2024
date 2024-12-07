import sys

def op_concat(a, b):
    return int(f"{a}{b}")

def test_eqn(target, intermediate, values, part2=False):
    if intermediate > target:
        return 0
    elif len(values) == 0:
        return target if intermediate == target else 0

    for op in [int.__add__, int.__mul__]:
        if test_eqn(target, op(intermediate, values[0]), values[1:], part2):
            return target

    if part2:
        if test_eqn(target, op_concat(intermediate, values[0]), values[1:], part2):
            return target

    return 0

part1 = 0
part2 = 0
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        answer, values = line.split(":")
        answer = int(answer)
        values = [int(v) for v in values.split()]

        part1 += test_eqn(answer, values[0], values[1:])
        part2 += test_eqn(answer, values[0], values[1:], True)

print(part1)
print(part2)

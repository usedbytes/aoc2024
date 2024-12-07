import sys

def test_eqn(target, intermediate, values):
    if intermediate > target:
        return 0
    elif len(values) == 0:
        return intermediate == target

    for op in [int.__add__, int.__mul__]:
        if test_eqn(target, op(intermediate, values[0]), values[1:]):
            return answer

    return 0

part1 = 0
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        answer, values = line.split(":")
        answer = int(answer)
        values = [int(v) for v in values.split()]

        part1 += test_eqn(answer, values[0], values[1:])
print(part1)

import re
import sys

mul_re = re.compile(r"mul\(([0-9]+),([0-9]+)\)")

part1 = 0
with open(sys.argv[1]) as f:
    program = f.read()

    matches = mul_re.findall(program)
    for match in matches:
        a, b = map(int, match)
        part1 += a * b
print(part1)

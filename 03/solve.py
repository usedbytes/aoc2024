import re
import sys

mul_re_str = r"(mul)\(([0-9]+),([0-9]+)\)"
do_re_str = r"(do)\(\)"
dont_re_str = r"(don\'t)\(\)"

full_re = re.compile(f"({do_re_str}|{dont_re_str}|{mul_re_str})")

part1 = 0
part2 = 0
with open(sys.argv[1]) as f:
    program = f.read()

    do = True

    matches = full_re.finditer(program)
    for match in matches:
        if match[2] == "do":
            do = True
        elif match[3] == "don't":
            do = False
        elif match[4] == "mul":
            product = int(match[5]) * int(match[6])
            part1 += product
            if do:
                part2 += product
print(part1)
print(part2)

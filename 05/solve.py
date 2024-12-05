import sys

rules = []

def check_update(update):
    for a, b in rules:
        if a in update and b in update:
            if update[a] > update[b]:
                return False
    return True

part1 = 0

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)
    for line in lines:
        if line == "":
            break

        a, b = map(int, line.split("|"))
        rules.append((a, b))

    print(f"{len(rules)=}")

    for line in lines:
        fields = list(map(int, line.split(",")))
        assert len(fields) == len(set(fields))

        # Permit look-up index by page number
        update = {
            v: i
            for i, v in enumerate(fields)
        }

        if check_update(update):
            val = fields[(len(fields))//2]
            part1 += val

print(part1)

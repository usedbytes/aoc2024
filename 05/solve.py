import sys

rules = []

def check_update(update):
    for a, b in rules:
        if a in update and b in update:
            if update[a] > update[b]:
                return False
    return True



def rebuild_update(fields):
    update = []

    for f in fields:
        applies = filter(lambda v: v[0] == f, rules)
        insert_idx = len(update)
        for a, b in applies:
            try:
                idx = update.index(b)
                insert_idx = min(idx, insert_idx)
            except ValueError:
                pass
        update.insert(insert_idx, f)

    return update

part1 = 0
part2 = 0

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)
    for line in lines:
        if line == "":
            break

        a, b = map(int, line.split("|"))
        rules.append((a, b))

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
        else:
            new_fields = rebuild_update(fields)
            val = new_fields[(len(new_fields))//2]
            part2 += val

print(part1)
print(part2)

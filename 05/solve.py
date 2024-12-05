import sys

from typing import List, Mapping, Tuple

def check_update(page_indices: Mapping[int, int], rules: List[Tuple[int, int]]) -> bool:
    for page_a, page_b in rules:
        if page_a in page_indices and page_b in page_indices:
            if page_indices[page_a] > page_indices[page_b]:
                return False
    return True

def rebuild_update(update: List[int], rules: List[Tuple[int, int]]) -> List[int]:
    result = []

    for page_a in update:
        rules_that_apply = filter(lambda rule: rule[0] == page_a, rules)

        # If unconstrained, insert at the end
        # I think this depends on the input being well-constrained?
        insert_idx = len(result)

        # Find the lowest index of a constraining page
        for _, page_b in rules_that_apply:
            try:
                # If page_b is already in the list, we must put page_a
                # before it
                idx = result.index(page_b)
                insert_idx = min(idx, insert_idx)
            except ValueError:
                pass

        # Insert below the lowest constraint
        result.insert(insert_idx, page_a)

    return result

part1 = 0
part2 = 0

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)

    # Get all the rules
    rules = []
    for line in lines:
        if line == "":
            break

        a, b = map(int, line.split("|"))
        rules.append((a, b))

    # Check all the updates
    for line in lines:
        update = list(map(int, line.split(",")))

        # Make sure there's no duplicate page numbers
        assert len(update) == len(set(update))

        # Map page number to index-in-update
        page_indices = {
            v: i
            for i, v in enumerate(update)
        }

        if check_update(page_indices, rules):
            val = update[(len(update))//2]
            part1 += val
        else:
            new_update = rebuild_update(update, rules)
            val = new_update[(len(new_update))//2]
            part2 += val

print(part1)
print(part2)

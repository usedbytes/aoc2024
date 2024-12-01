import sys

from collections import defaultdict

a_list, b_list = [], []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        a, b = line.split()
        a_list.append(int(a))
        b_list.append(int(b))

    # First sort both lists
    a_list.sort()
    b_list.sort()

    # Then get their pairwise differences
    diff_list = []
    for a, b in zip(a_list, b_list):
        diff_list.append(abs(b - a))

    part1 = sum(diff_list)
    print(part1)

    # Track frequency histogram
    hist = defaultdict(int)
    for v in b_list:
        hist[v] += 1

    products = map(lambda a: a * hist[a], a_list)

    part2 = sum(products)
    print(part2)

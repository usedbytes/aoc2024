import sys

a_list, b_list = [], []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        a, b = line.split()
        a_list.append(int(a))
        b_list.append(int(b))

    a_list.sort()
    b_list.sort()

    diff_list = []
    for a, b in zip(a_list, b_list):
        diff_list.append(abs(b - a))
    print(sum(diff_list))

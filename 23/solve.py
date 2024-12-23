import sys

from collections import defaultdict

nmap = defaultdict(set)

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        a, b = line.split("-")

        nmap[a].add(b)
        nmap[b].add(a)

triples = set()
for a, al in nmap.items():
    if a[0] != "t":
        continue
    if len(al) < 2:
        continue

    for b in al:
        bl = nmap[b]
        if len(bl) < 2:
            continue
        for c in bl:
            cl = nmap[c]

            if a in cl:
                triple = tuple(sorted((a, b, c)))
                triples.add(triple)

p1 = len(triples)
print(p1)

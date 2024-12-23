import sys

from collections import defaultdict

nmap = defaultdict(set)

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        a, b = line.split("-")

        nmap[a].add(b)
        nmap[b].add(a)

def find_clique(a, nmap, clique=None, seen=None):
    this = set(nmap[a])
    this.add(a)

    if seen is None:
        seen = set()
    if clique is None:
        clique = this
    else:
        clique.intersection_update(this)

    seen.add(a)

    for b in set(clique):
        if b not in seen and b in clique:
            find_clique(b, nmap, clique, seen)

    return clique

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

cliques = []
for a in nmap.keys():
    clique = find_clique(a, nmap)
    cliques.append(clique)

cliques.sort(key=lambda v: len(v))

p2 = sorted(cliques[-1])
print(",".join(p2))

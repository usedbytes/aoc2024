import sys

def do_hash(x):
    a = (x ^ (x << 6)) & 0xffffff
    b = (a ^ (a >> 5)) & 0xffffff
    c = (b ^ (b << 11)) & 0xffffff
    return c

buyers = []
p1 = 0
with open(sys.argv[1]) as f:
    for n in map(int, f):
        prices = [n % 10]
        for i in range(2000):
            n = do_hash(n)
            prices.append(n % 10)
        p1 += n
        buyers.append(prices)
print(p1)

# Find all possible sequences and their prices
buyer_seqs = []
for prices in buyers:
    seqs = {}
    for i, v in enumerate(prices[4:]):
        seq = (
            prices[i + 1] - prices[i + 0],
            prices[i + 2] - prices[i + 1],
            prices[i + 3] - prices[i + 2],
            prices[i + 4] - prices[i + 3],
        )
        if seq in seqs:
            continue
        seqs[seq] = v
    buyer_seqs.append(seqs)

# All unique sequences
u = set()
for b in buyer_seqs:
    u.update(b.keys())

# Brute force best prices
p2 = 0
for seq in u:
    total_price = 0
    for buyer in buyer_seqs:
        total_price += buyer.get(seq, 0)
    p2 = max(p2, total_price)
print(p2)

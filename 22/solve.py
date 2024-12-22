import sys

def do_hash(number):
    number = (number ^ (number * 64)) & 0xffffff
    number = (number ^ (number // 32)) & 0xffffff
    number = (number ^ (number * 2048)) & 0xffffff

    return number

p1 = 0
with open(sys.argv[1]) as f:
    for n in map(int, f):
        for i in range(2000):
            n = do_hash(n)
        p1 += n
print(p1)

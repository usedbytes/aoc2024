import sys

from collections import namedtuple

wires = {}
gates = {}

Gate = namedtuple("Gate", "a op b")

with open(sys.argv[1]) as f:
    lines = map(str.strip, f)
    while True:
        line = next(lines)
        if line == "":
            break

        wire, value = line.split(": ")
        value = int(value)
        wires[wire] = value

    for line in lines:
        a, op, b, _, c = line.split()
        gates[c] = Gate(a, op, b)

while True:
    resolved = 0
    for signal in list(gates.keys()):
        gate = gates[signal]

        if gate.a not in wires or gate.b not in wires:
            continue

        del gates[signal]
        resolved += 1

        a = wires[gate.a]
        b = wires[gate.b]
        c = signal
        match gate.op:
            case "AND":
                wires[c] = a & b
            case "OR":
                wires[c] = a | b
            case "XOR":
                wires[c] = a ^ b
    if resolved == 0:
        break

assert len(gates) == 0

z_keys = list(filter(lambda v: v[0] == "z", wires.keys()))
z_keys.sort()
p1 = 0
for bit, k in enumerate(z_keys):
    p1 |= wires[k] << bit
print(p1)


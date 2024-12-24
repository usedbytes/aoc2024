import sys

from collections import namedtuple

wires = {}
gates = {}

Gate = namedtuple("Gate", "a b op c")

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
        gates[c] = Gate(min(a, b), max(a, b), op, c)

nbits = len(wires) // 2
orig_wires = wires.copy()
orig_gates = gates.copy()

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

# Maps (in, in, op) -> Gate
# Inputs are sorted first.
gate_map = {}
for signal, gate in orig_gates.items():
    gate_map[(
        gate.a,
        gate.b,
        gate.op
    )] = gate

def get_gate(a, b, op):
    return gate_map.get((min(a, b), max(a, b), op))

def find_and_xor_pair(x):
    gates = []
    inputs = set()
    for gate in orig_gates.values():
        if gate.a == x or gate.b == x:
            inputs.add(gate.a)
            inputs.add(gate.b)
            gates.append(gate)

    gates.sort()

    if (
        len(inputs) != 2 or
        len(gates) != 2 or
        gates[0].op != "AND" or
        gates[1].op != "XOR"
    ):
        return None

    return gates

def remap(a):
    return remaps.get(a, a)

carry_outs = []
half_adds = []
half_carries = []
remaps = {}

for bit in range(nbits):
    # Input AND -> half carry
    half_and = get_gate(f"x{bit:02d}", f"y{bit:02d}", "AND")
    assert half_and is not None
    half_carries.append(half_and.c)

    # Input OR -> half add
    half_xor = get_gate(f"x{bit:02d}", f"y{bit:02d}", "XOR")
    assert half_xor is not None
    half_adds.append(half_xor.c)

    if bit == 0:
        carry_outs.append(half_and.c)
        assert half_xor.c == f"z{bit:02d}"
    else:
        # Look for output and carry out
        a = remap(half_adds[bit])
        b = remap(carry_outs[bit - 1])
        out = get_gate(a, b, "XOR")

        if out is None:
            # Either a or b is wrong (hopefully not both?!)
            # We should be able to find an AND and an XOR with the same inputs,
            # where one of those inputs is 'a' or 'b'
            pair = find_and_xor_pair(a)
            if pair is not None:
                # b is the bad one
                if pair[0].a == a:
                    remapped = pair[0].b
                else:
                    remapped = pair[0].a
                remaps[b] = remapped
                remaps[remapped] = b
            else:
                # a is the bad one
                pair = find_and_xor_pair(b)
                assert pair is not None

                if pair[0].a == a:
                    remapped = pair[0].a
                else:
                    remapped = pair[0].b
                remaps[a] = remapped
                remaps[remapped] = a

            # Update inputs according to new mapping
            a = remap(a)
            b = remap(b)
            out = get_gate(a, b, "XOR")

        expected_out = f"z{bit:02d}"
        if out.c != expected_out:
            # For output gates, we know what the output should be - fix if wrong
            remaps[out.c] = expected_out
            remaps[expected_out] = out.c

        other_carry = get_gate(a, b, "AND")
        carry_out = get_gate(remap(half_carries[bit]), remap(other_carry.c), "OR")

        # Make sure we found all the gates
        assert out and other_carry and carry_out

        carry_outs.append(carry_out.c)

assert len(remaps.keys()) == 8

print(",".join(sorted(remaps.keys())))

import sys

from typing import List

class MachineState:
    a: int
    b: int
    c: int
    pc: int
    program: List[int]
    out_buf: List[int]

    def __str__(self):
        return f"a={self.a} b={self.b} c={self.c}; pc={self.pc}, out_buf={self.out_buf}"

    def __init__(self, a, b, c, pc, program):
        self.a = a
        self.b = b
        self.c = c
        self.pc = pc
        self.program = program
        self.out_buf = []

        self.isa = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]

    def __decode_combo(self, combo):
        assert combo < 7

        if combo < 4:
            return combo
        elif combo == 4:
            return self.a
        elif combo == 5:
            return self.b
        elif combo == 6:
            return self.c

    def adv(self, combo):
        num = self.a
        den = 2 ** self.__decode_combo(combo)
        self.a = num // den
        self.pc += 2

    def bxl(self, literal):
        self.b ^= literal
        self.pc += 2

    def bst(self, combo):
        self.b = self.__decode_combo(combo) & 0x7
        self.pc += 2

    def jnz(self, literal):
        if self.a != 0:
            self.pc = literal
        else:
            self.pc += 2

    def bxc(self, ignored):
        self.b = self.b ^ self.c
        self.pc += 2

    def out(self, combo):
        val = self.__decode_combo(combo) & 0x7
        self.out_buf.append(val)
        self.pc += 2

    def bdv(self, combo):
        num = self.a
        den = 2 ** self.__decode_combo(combo)
        self.b = num // den
        self.pc += 2

    def cdv(self, combo):
        num = self.a
        den = 2 ** self.__decode_combo(combo)
        self.c = num // den
        self.pc += 2

    def run(self):
        while self.pc < len(self.program):
            opcode, arg = self.program[self.pc], self.program[self.pc + 1]
            op = self.isa[opcode]
            op(arg)

    def get_output(self):
        return ",".join(map(str, self.out_buf))

with open(sys.argv[1]) as f:
    init_state = {
        "pc": 0,
    }
    for line in map(str.strip, f):
        if len(line) == 0:
            continue

        if line.startswith("Register"):
            _, regname, val = line.split()
            regname = regname[0].lower()
            val = int(val)
            init_state[regname] = val
        elif line.startswith("Program"):
            _, prog = line.split()
            init_state["program"] = [int(v) for v in prog.split(",")]
    machine = MachineState(**init_state)

machine.run()
p1 = machine.get_output()
print(p1)

def part2_slow():
    # This should work, but seems like it will take to the heat-death of the
    # universe
    program = init_state["program"]
    init_a = 0
    while True:
        init_a += 1
        a = init_a
        b = 0
        c = 0
        result = []
        if init_a % 1000000 == 0:
            print(".", end="")
        if init_a % 10000000 == 0:
            print(init_a)
        for i in range(len(program)):
            b = a & 0x7
            b ^= 1
            c = a // 2**b
            b = b ^ c
            b = b ^ 4
            result.append(b & 0x7)
            if b & 0x7 != program[i]:
                break
            a = a // 8
        if result == program:
            print(init_a, result)
            break

# By the power of crafted inputs...
# My program is a single loop. The only state that carries from one iteration
# to the next is 'a', and it's divided by 8 each loop.
#
#    b = a & 0x7
#    b ^= 1
#    c = a // 2**b
#    b = b ^ c
#    a = a // 8
#    b = b ^ 4
#    out b & 0x7
#    jnz 0
#
# So, we can work from end to start:
#   - Find the lowest value of 'a' which gives the right value for the last output
#   - Multiply that 'a' value by 8
#   - Use that result as the starting value, try adding 1 until the resulting
#     output is the correct last 2 values
#   - Multiply that by 8...
#   - Repeat until you complete the program
program = init_state["program"]
init_a = 0
for i in range(len(program)):
    # Determined this by inspection of my program.
    # The only mutation of a is divide by 8 before the loop
    init_a *= 8
    while True:
        machine = MachineState(**init_state)
        machine.a = init_a
        machine.run()
        if machine.out_buf == program[-(i + 1):]:
            break
        init_a += 1
print(init_a)

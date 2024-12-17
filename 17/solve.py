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

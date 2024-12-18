from collections import deque, namedtuple
import sys
import re

btn_re = re.compile(r"X(.*), Y(.*)")
prize_re = re.compile(r"X=(.*), Y=(.*)")

Matrix = namedtuple("Matrix", "a b c d")

def do_claw(a_step, b_step, prize):
    m = Matrix(a_step[0], b_step[0], a_step[1], b_step[1])

    denominator = m.a * m.d - m.b * m.c

    # Partial inverse - not divided by determinant
    m_ip = Matrix(m.d, -m.b, -m.c, m.a)

    a = (m_ip.a * prize[0] + m_ip.b * prize[1]) // denominator
    b = (m_ip.c * prize[0] + m_ip.d * prize[1]) // denominator

    if a * a_step[0] + b * b_step[0] == prize[0] and \
        a * a_step[1] + b * b_step[1] == prize[1]:
            return (a, b)

    return None

p1 = 0
p2 = 0
with open(sys.argv[1]) as f:
    try:
        while True:
            lines = map(str.strip, f)
            a_line = next(lines)[10:]
            match = btn_re.fullmatch(a_line)
            a_step = (int(match.group(1)), int(match.group(2)))

            b_line = next(lines)[10:]
            match = btn_re.fullmatch(b_line)
            b_step = (int(match.group(1)), int(match.group(2)))

            prize_line = next(lines)[7:]
            match = prize_re.fullmatch(prize_line)
            prize = (int(match.group(1)), int(match.group(2)))

            presses = do_claw(a_step, b_step, prize)
            if presses is not None:
                a, b = presses
                p1 += (3 * a) + b

            presses = do_claw(a_step, b_step, (prize[0] + 10000000000000, prize[1] + 10000000000000))
            if presses is not None:
                a, b = presses
                p2 += (3 * a) + b

            _ = next(lines)
    except StopIteration:
        pass
print(p1)
print(p2)

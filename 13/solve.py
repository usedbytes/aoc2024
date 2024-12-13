from collections import deque
import sys
import re

btn_re = re.compile(r"X(.*), Y(.*)")
prize_re = re.compile(r"X=(.*), Y=(.*)")

p1 = 0
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

            start = (0, 0)
            queue = deque()
            queue.append(((start[0] + a_step[0], start[1] + b_step[1]), (1, 0)))
            queue.append(((start[0] + b_step[0], start[1] + b_step[1]), (0, 1)))

            min_steps = None
            seen = set()
            while len(queue) > 0:
                (px, py), (a, b) = queue.popleft()
                if (px, py) == prize:
                    min_steps = (a, b)
                    break

                next_a = (px + a_step[0], py + a_step[1])
                if next_a not in seen and a < 101:
                    seen.add(next_a)
                    queue.append((next_a, (a + 1, b)))

                next_b = (px + b_step[0], py + b_step[1])
                if next_b not in seen and b < 101:
                    seen.add(next_b)
                    queue.append((next_b, (a, b + 1)))

            if min_steps is not None:
                a, b = min_steps
                p1 += (3 * a) + b

            _ = next(lines)
    except StopIteration:
        pass
print(p1)

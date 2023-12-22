from collections import defaultdict
from itertools import chain

from run_util import run_puzzle
import re


def parse_data(data: str):
    bricks = []
    for row in data.split('\n'):
        positions = set()
        sx, sy, sz, ex, ey, ez = re.search(r"([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)", row).groups()
        for x in range(int(sx), int(ex) + 1):
            for y in range(int(sy), int(ey) + 1):
                positions.add((x, y))

        bricks.append([positions, int(sz), int(ez)])

    bricks.sort(key=lambda brick: brick[1])

    return bricks


def part_a(data: str) -> int:
    bricks = parse_data(data)
    original_bricks = parse_data(data)
    above_bricks = defaultdict(lambda: set())
    below_bricks = defaultdict(lambda: set())
    for index, brick in enumerate(bricks):
        positions, sz, ez = brick

        new_sz = None

        on_bricks = set()
        for lower in range(index - 1, -1, -1):
            other_positions, osz, esz = bricks[lower]
            updated_sz = max(osz + 1, esz + 1)

            if positions.intersection(other_positions) and (new_sz is None or updated_sz >= new_sz):
                if new_sz is None or updated_sz < new_sz:
                    on_bricks = {lower}
                elif updated_sz == new_sz:
                    on_bricks.add(lower)

                new_sz = updated_sz

        for is_on in on_bricks:
            above_bricks[is_on].add(index)
        below_bricks[index] = on_bricks
        if new_sz is None:
            new_sz = 1
        brick[1] = new_sz
        brick[2] = new_sz + ez - sz

    can_be_removed = set()
    for index in range(len(bricks)):
        provides_support_for = above_bricks[index]
        if len(provides_support_for) == 0:
            can_be_removed.add(index)
        if len(below_bricks[index]) > 1:
            for brick in below_bricks[index]:
                can_be_removed.add(brick)

    return len(can_be_removed)


def part_b(data: str) -> int:
    data = parse_data(data)
    return 0


def main():
    examples = [
        ("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""", 5, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

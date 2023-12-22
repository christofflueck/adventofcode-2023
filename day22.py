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

    # Sort by the end Z position
    bricks.sort(key=lambda brick: brick[2])

    return bricks


def part_a(data: str) -> int:
    bricks = parse_data(data)
    original_bricks = parse_data(data)
    above_bricks = defaultdict(lambda: set())
    below_bricks = defaultdict(lambda: set())

    # Loop over the already sorted bricks
    for index, brick in enumerate(bricks):
        positions, sz, ez = brick

        new_ez = None

        on_bricks = set()
        # Check all bricks below
        for lower in range(index - 1, -1, -1):
            other_positions, osz, esz = bricks[lower]
            updated_ez = esz + 1

            # if it overlaps or if we found a new higher z value
            if positions.intersection(other_positions) and (new_ez is None or updated_ez >= new_ez):
                # Store all bricks this relies on
                if new_ez is None or updated_ez < new_ez:
                    # Either we haven't found a position or we found a new one. Refresh the set
                    on_bricks = {lower}
                elif updated_ez == new_ez:
                    # Same height so add to this position
                    on_bricks.add(lower)

                new_ez = updated_ez

        # Add this bricks to the list of bricks above the ones we're on
        for is_on in on_bricks:
            above_bricks[is_on].add(index)
        # Set the bricks this sits on
        below_bricks[index] = on_bricks
        # No intersections found -> on the floor
        if new_ez is None:
            new_ez = 1
        # Update the new z position of this brick
        brick[1] = new_ez - ez + sz
        brick[2] = new_ez

    # Check which bricks we can and can't remove
    can_be_removed = set()
    cannot_be_removed = set()
    for index in range(len(bricks)):
        provides_support_for = above_bricks[index]

        # add it if it doesn't provide support for any bricks
        if len(provides_support_for) == 0:
            can_be_removed.add(index)

        # If this sits on multiple bricks add all of them
        if len(below_bricks[index]) > 1:
            for brick in below_bricks[index]:
                can_be_removed.add(brick)

        # Make sure it the support brick doesn't get removed when it's the only one
        if len(below_bricks[index]) == 1:
            cannot_be_removed.add(list(below_bricks[index])[0])

    return len(can_be_removed - cannot_be_removed)


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

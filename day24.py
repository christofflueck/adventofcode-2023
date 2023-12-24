from run_util import run_puzzle
import re
import numpy as np


def parse_data(data: str):
    stones = []
    for row in data.split('\n'):
        px, py, pz, vx, vy, vz = re.search(
            r"([0-9]+),\s+([0-9]+),\s+([0-9]+)\s@\s+(\-?[0-9]+),\s+(\-?[0-9]+),\s+(\-?[0-9]+)", row).groups()
        stones.append((int(px), int(py), int(pz), int(vx), int(vy), int(vz)))
    return stones


def intersect_2d(v1, v2):
    px1, py1, _, vx1, vy1, _ = v1
    px2, py2, _, vx2, vy2, _ = v2

    #  s * vx1 - r * vx2 = px2 - px1
    #  s * vy1 - r * vy2 = py2 - py1
    det_a = vx1 * (-vy2) - (-vx2) * vy1

    if det_a == 0:
        return None

    r = ((px2 - px1) * (-vy2) - (py2 - py1) * (-vx2)) / det_a
    s = (vx1 * (py2 - py1) - vy1 * (px2 - px1)) / det_a

    # Only go forward
    if r < 0 or s < 0:
        return None

    x = px1 + r * vx1
    y = py2 + s * vy2

    return x, y

def collision_time(v1, v2):
    px1, py1, pz1, vx1, vy1, vz1 = v1
    px2, py2, pz2, vx2, vy2, vz2 = v2

    #  s * vx1 - r * vx2 = px2 - px1
    #  s * vy1 - r * vy2 = py2 - py1
    #  s * vz1 - r * vz2 = pz2 - pz1
    det_a = vx1 * (-vy2) - (-vx2) * vy1

    if det_a == 0:
        return None

    r = ((px2 - px1) * (-vy2) - (py2 - py1) * (-vx2)) / det_a
    s = (vx1 * (py2 - py1) - vy1 * (px2 - px1)) / det_a

    if pz1 + r * vz1 != pz2 + s * vz2:
        return None

    # Only go forward
    if (r < 0 or s < 0) and r != s:
        return None

    return r


def part_a(data: str) -> int:
    stones = parse_data(data)

    min_c, max_c = (200000000000000, 400000000000000)
    if len(stones) == 5:
        min_c, max_c = (7, 27)
    intersections = 0

    for index, stone in enumerate(stones):
        for other_index in range(index + 1, len(stones)):
            other_stone = stones[other_index]
            intersection = intersect_2d(stone, other_stone)
            if intersection is not None:
                x, y = intersection
                if min_c <= x <= max_c and min_c <= y <= max_c:
                    intersections += 1

    return intersections


def part_b(data: str) -> int:
    stones = parse_data(data)

    throw = (24, 13, 10, -3, 1, 2)
    i0 = collision_time(throw, stones[0])
    i1 = collision_time(throw, stones[1])
    i2 = collision_time(throw, stones[2])

    return 0


def main():
    examples = [
        ("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""", 2, 47)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

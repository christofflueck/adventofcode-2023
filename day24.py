from run_util import run_puzzle
import re
import z3


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

    x, y, z = z3.BitVecs("x y z", 64)
    vx, vy, vz = z3.BitVecs("vx vy vz", 64)

    solver = z3.Solver()

    for index, stone in enumerate(stones[:3]):
        t_index = z3.BitVec("t" + str(index), 64)
        px, py, pz, pvx, pvy, pvz = stone
        solver.add(t_index >= 0)
        solver.add(x + t_index * vx == px + t_index * pvx)
        solver.add(y + t_index * vy == py + t_index * pvy)
        solver.add(z + t_index * vz == pz + t_index * pvz)

    solver.check()
    solution = solver.model()

    val_x = solution[x].as_long()
    val_y = solution[y].as_long()
    val_z = solution[z].as_long()

    return val_x + val_y + val_z


def main():
    examples = [
        ("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""", 2, None)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

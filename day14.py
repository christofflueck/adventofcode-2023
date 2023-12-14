import functools

from tqdm import tqdm

from run_util import run_puzzle
import numpy as np


def parse_data(data: str):
    return [list(row) for row in data.split('\n')]


def compare_values(a: str, b: str):
    if a == b or a == '#' or b == '#':
        return 0
    if a == 'O' and b == '.':
        return -1
    if a == '.' and b == 'O':
        return 1
    print('missing case for', a, b)


def part_a(data: str) -> int:
    data = parse_data(data)

    # current orientation = up is on up
    data = np.rot90(data, k=1)
    # current orientation = up is on the left

    for i in range(len(data)):
        str_row = "#".join(["".join(sorted(segment, reverse=True)) for segment in "".join(data[i]).split('#')])
        data[i] = np.array(list(str_row))

    # current orientation = up is on up
    data = np.rot90(data, k=3)


    load = 0
    for x, row in enumerate(data):
        load += (row == 'O').sum() * (len(data) - x)

    return load


def part_b(data: str) -> int:
    data = parse_data(data)

    for row in data:
        print("".join(row))
    print('---------------------')
    # current orientation = up is on up
    data = np.rot90(data, k=1)
    # current orientation = up is on the left

    indexes = {}
    grids = {}

    repeated_on = 0

    for cycle in tqdm(range(1000000000)):
        data = np.rot90(data, k=3)
        if data.tobytes() in indexes:
            repeated_on = cycle
            print('FOUND REPEAT AT', cycle)
            break
        else:
            grids[data.tobytes()] = cycle
        for i in range(len(data)):
            str_row = "#".join(["".join(sorted(segment, reverse=True)) for segment in "".join(data[i]).split('#')])
            data[i] = np.array(list(str_row))

    # current orientation = up is on up
    data = np.rot90(data, k=3)

    load = 0
    for x, row in enumerate(data):
        load += (row == 'O').sum() * (len(data) - x)

    return load


def main():
    examples = [
        ("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""", 136, 64)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

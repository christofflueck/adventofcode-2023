from tqdm import tqdm

from run_util import run_puzzle


def turn_left(data):
    return tuple(["".join([data[row][len(data) - 1 - col] for row in range(len(data))]) for col in range(len(data))])


def turn_right(data):
    return tuple(["".join([data[len(data) - 1 - row][col] for row in range(len(data))]) for col in range(len(data))])


def print_correct_way_up(data, times_turned):
    print_data = data
    print("TURNED", times_turned)
    for _ in range((times_turned + 1) % 4):
        print_data = turn_left(print_data)
    for row in print_data:
        print(row)


def parse_data(data: str):
    split = data.split('\n')
    return turn_left(split)


def tilt_left(data):
    for _ in range(len(data[0])):
        data = [row.replace('.O', 'O.') for row in data]
    return tuple(data)


def part_a(data: str) -> int:
    data = parse_data(data)

    data = tilt_left(data)

    load = 0
    for x in range(len(data[0])):
        load += [row[x] for y, row in enumerate(data)].count('O') * (len(data) - x)

    return load


def part_b(data: str) -> int:
    data = parse_data(data)

    lookup = {}
    reverse = {}
    cycle = 0

    for cycle in range(1000000000):
        reverse[cycle] = data

        if data not in lookup:
            lookup[data] = cycle
        else:
            break

        for i in range(4):
            data = turn_right(tilt_left(data))

    diff = (1000000000 - lookup[data]) % (cycle - lookup[data])
    data = reverse[lookup[data] + diff]
    load = 0
    for x in range(len(data[0])):
        load += [row[x] for y, row in enumerate(data)].count('O') * (len(data) - x)

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

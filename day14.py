from run_util import run_puzzle


def parse_data(data: str):
    return [list(row) for row in data.split('\n')]


def part_a(data: str) -> int:
    data = parse_data(data)

    # tilt down
    for x in range(len(data[0])):
        for y in range(len(data)):
            if data[y][x] == 'O':
                print('Found 0 at', y, x)
                target = -1
                for i in range(y - 1, -1, -1):
                    if data[i][x] == '#':
                        break
                    if data[i][x] == '.':
                        target = i
                print('Moving it to', target, x)
                if target >= 0:
                    data[target][x] = 'O'
                    data[y][x] = '.'
        print('---------------------')
        for row in data:
            print(''.join(row))

    load = 0

    for x, row in enumerate(data):
        load += row.count('O') * (len(data) - x)

    return load


def part_b(data: str) -> int:
    data = parse_data(data)
    return 0


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
#OO..#....""", 136, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

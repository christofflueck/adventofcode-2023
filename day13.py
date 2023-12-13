from run_util import run_puzzle


def parse_pattern(data):
    str_rows = data.split('\n')
    rows = [int(x, 2) for x in str_rows]
    str_cols = [''.join([row[i] for row in str_rows]) for i in range(len(str_rows[0]))]
    cols = [int(x, 2) for x in str_cols]
    return cols, rows


def parse_data(data: str):
    data = data.replace('#', '1').replace('.', '0')
    patterns = []
    for pattern in data.split('\n\n'):
        patterns.append(parse_pattern(pattern))
    return patterns


def part_a(data: str) -> int:
    patterns = parse_data(data)

    lefts = []
    aboves = []
    for cols, rows in patterns:
        prev = -1

        for i, col in enumerate(cols):
            if col == prev:
                lefts.append(i - 1)
                break
            prev = col

    return 0


def part_b(data: str) -> int:
    data = parse_data(data)
    return 0


def main():
    examples = [
        ("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""", 405, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

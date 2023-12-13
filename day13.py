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
        left_mirror = count_mirrors(cols, False)
        if left_mirror:
            lefts.append(left_mirror)
        above_mirror = count_mirrors(rows, False)
        if above_mirror:
            aboves.append(above_mirror)

    return sum(lefts) + sum(aboves * 100)


def count_mirrors(cols, smudge):
    prev = -9999
    for i, col in enumerate(cols):
        if i == 0:
            prev = col
            continue
        left = prev
        right = col

        success = False
        counter = 0
        smudge_counter = 0
        while left == right or (smudge and bin(left ^ right).count('1') == 1):
            counter += 1
            if bin(left ^ right).count('1') == 1:
                smudge_counter += 1
            if i - counter > 0 and i + counter < len(cols):
                left = cols[i - counter - 1]
                right = cols[i + counter]
            else:
                success = True
                break

        if success and (not smudge or smudge_counter == 1):
            return i
        prev = col


def part_b(data: str) -> int:
    patterns = parse_data(data)

    lefts = []
    aboves = []
    for cols, rows in patterns:
        left_mirror = count_mirrors(cols, True)
        if left_mirror:
            lefts.append(left_mirror)
        above_mirror = count_mirrors(rows, True)
        if above_mirror:
            aboves.append(above_mirror)
        if not left_mirror and not above_mirror:
            print('No match found')

    return sum(lefts) + sum(aboves * 100)


def main():
    examples = [
        ("""..#..##..#..#...#
#.#..##.#....#.##
##.#...###..###..
##...#..##..##..#
#.###.##.####.##.
###...##..##..##.
######..######..#
######..######..#
###...##..##..##.
#.###.##.####.##.
##...#..##..##..#""", None, 11)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

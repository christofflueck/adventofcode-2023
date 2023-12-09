from run_util import run_puzzle


def part_a(data: str) -> int:
    rows = [[int(x) for x in row.split()] for row in data.split('\n')]

    added = []

    for row in rows:
        histories = [row]
        while not all([x == 0 for x in histories[-1]]):
            histories.append([histories[-1][i + 1] - histories[-1][i] for i in range(len(histories[-1]) - 1)])

        added_value = 0
        for val in reversed(histories):
            added_value += val[-1]

        added.append(added_value)

    return sum(added)


def part_b(data: str) -> int:
    rows = [[int(x) for x in row.split()] for row in data.split('\n')]

    added = []

    for row in rows:
        histories = [row]
        while not all([x == 0 for x in histories[-1]]):
            histories.append([histories[-1][i + 1] - histories[-1][i] for i in range(len(histories[-1]) - 1)])

        added_value = 0
        for val in reversed(histories):
            added_value = val[0] - added_value

        added.append(added_value)

    return sum(added)


def main():
    examples = [
        ("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""", 114, 2)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

from run_util import run_puzzle


def part_a(data: str):
    filtered_rows = [[d for d in x if d.isnumeric()] for x in data.split('\n')]

    numbers = [int(r[0] + r[-1]) for r in filtered_rows if len(r) > 0]

    return sum(numbers)


DIGITS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def part_b(data: str):
    str_rows = data.split('\n')
    filtered_rows = []

    for row in str_rows:
        filtered_row = []
        for i, char in enumerate(row):
            if char.isnumeric():
                filtered_row.append(int(char))
            for num, digit in enumerate(DIGITS):
                if row[i:].startswith(digit):
                    filtered_row.append(num+1)
        filtered_rows.append(filtered_row)

    numbers = [10* r[0] + r[-1] for r in filtered_rows]
    return sum(numbers)


def main():
    examples = [
        ("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""", 209, 281)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

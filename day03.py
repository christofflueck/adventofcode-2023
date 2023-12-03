from run_util import run_puzzle


def part_a(data: str):
    rows = [x for x in data.split('\n')]
    numbers = []
    added = set()

    for y in range(len(rows)):
        row = rows[y]
        for x in range(len(row)):
            cell = row[x]

            if not cell.isnumeric() and cell != '.':
                neighbors = {(max(0, y - 1), max(0, x - 1)),
                             (max(0, y - 1), max(0, x)),
                             (max(0, y - 1), min(len(row), x + 1)),
                             (max(0, y), max(0, x - 1)),
                             (max(0, y), min(len(row), x + 1)),
                             (min(len(rows), y + 1), max(0, x - 1)),
                             (min(len(rows), y + 1), max(0, x)),
                             (min(len(rows), y + 1), min(len(row), x + 1))}

                for neighbor in neighbors:
                    if neighbor in added:
                        continue
                    neighbor_value = rows[neighbor[0]][neighbor[1]]
                    if neighbor_value.isnumeric():
                        added.add(neighbor)
                        digits = neighbor_value
                        ny, nx = neighbor
                        lx = nx - 1
                        rx = nx + 1
                        while lx >= 0 and rows[neighbor[0]][lx].isnumeric():
                            digits = rows[neighbor[0]][lx] + digits
                            added.add((ny, lx))
                            lx -= 1
                        while rx < len(rows[neighbor[0]]) and rows[neighbor[0]][rx].isnumeric():
                            digits = digits + rows[neighbor[0]][rx]
                            added.add((ny, rx))
                            rx += 1
                        numbers.append(int(digits))

    return sum(numbers)


def part_b(data):
    rows = [x for x in data.split('\n')]
    numbers = []
    added = set()

    for y in range(len(rows)):
        row = rows[y]
        for x in range(len(row)):
            cell = row[x]

            if cell == '*':
                neighbors = {(max(0, y - 1), max(0, x - 1)),
                             (max(0, y - 1), max(0, x)),
                             (max(0, y - 1), min(len(row), x + 1)),
                             (max(0, y), max(0, x - 1)),
                             (max(0, y), min(len(row), x + 1)),
                             (min(len(rows), y + 1), max(0, x - 1)),
                             (min(len(rows), y + 1), max(0, x)),
                             (min(len(rows), y + 1), min(len(row), x + 1))}
                gear_ratios = []

                for neighbor in neighbors:
                    if neighbor in added:
                        continue
                    neighbor_value = rows[neighbor[0]][neighbor[1]]
                    if neighbor_value.isnumeric():
                        added.add(neighbor)
                        digits = neighbor_value
                        ny, nx = neighbor
                        lx = nx - 1
                        rx = nx + 1
                        while lx >= 0 and rows[neighbor[0]][lx].isnumeric():
                            digits = rows[neighbor[0]][lx] + digits
                            added.add((ny, lx))
                            lx -= 1
                        while rx < len(rows[neighbor[0]]) and rows[neighbor[0]][rx].isnumeric():
                            digits = digits + rows[neighbor[0]][rx]
                            added.add((ny, rx))
                            rx += 1
                        gear_ratios.append(int(digits))

                if len(gear_ratios) == 2:
                    numbers.append(gear_ratios[0] * gear_ratios[1])

    return sum(numbers)


def main():
    examples = [
        ("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""", 4361, 467835)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

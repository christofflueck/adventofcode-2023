from run_util import run_puzzle
import re


def part_a(data: str) -> int:
    added_distance = 1
    expanded_galaxies = parse_data(added_distance, data)
    distances = get_distances(expanded_galaxies)

    return sum(distances)


def get_distances(expanded_galaxies):
    distances = []
    for src, coords in enumerate(expanded_galaxies):
        for dest in range(src, len(expanded_galaxies)):
            distances.append(abs(coords[0] - expanded_galaxies[dest][0]) + abs(coords[1] - expanded_galaxies[dest][1]))
    return distances


def parse_data(added_distance, data):
    str_rows = data.split('\n')
    galaxies = [[m.start() for m in re.finditer('#', x)] for x in str_rows]
    empty_rows = [i for i, x in enumerate(galaxies) if len(x) == 0]
    empty_columns = [i for i in range(len(str_rows[0])) if all([i not in row for row in galaxies])]
    expanded_galaxies = []
    for y, row in enumerate(galaxies):
        for x in row:
            expanded_y = y + sum([added_distance for expanded_row in empty_rows if expanded_row < y])
            expanded_x = x + sum([added_distance for expanded_col in empty_columns if expanded_col < x])
            expanded_galaxies.append((expanded_x,
                                      expanded_y))
    return expanded_galaxies


def part_b(data: str) -> int:
    added_distance = 999_999
    expanded_galaxies = parse_data(added_distance, data)
    distances = get_distances(expanded_galaxies)

    return sum(distances)


def main():
    examples = [
        ("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 374, 82000210)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

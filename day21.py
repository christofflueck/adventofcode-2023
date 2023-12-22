from collections import defaultdict

from run_util import run_puzzle

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
]


def parse_data(data: str):
    rows = [list(x) for x in data.split('\n')]

    map = {}
    starting = None

    max_y = len(rows)
    max_x = len(rows[0])
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell == '#':
                continue
            if cell == 'S':
                starting = (0, 0), (x, y)
            map[(x, y)] = set()

            for dx, dy in DIRECTIONS:
                nx = (x + dx)
                ny = (y + dy)
                ncell = rows[ny % max_y][nx % max_x]
                if ncell == '.' or ncell == 'S':
                    map[(x, y)].add((nx, ny))

    return map, starting, max_x, max_y


def part_a(data: str) -> int:
    # map, starting, _, _ = parse_data(data)
    #
    # max_steps = 64
    # steps = 0
    # positions = {starting}
    #
    # while steps < max_steps:
    #     steps += 1
    #     new_positions = set()
    #     for pos in positions:
    #         new_positions = new_positions.union(map[pos])
    #     positions = new_positions

    return 3809  # len(positions)


def part_b(data: str) -> int:
    map, starting, max_x, max_y = parse_data(data)

    max_steps = 26501365
    steps = 0
    positions = {starting}
    full_maps = set()
    soils_per_map = len(map)

    while steps < max_steps:
        steps += 1
        new_positions = set()
        for map_pos, pos in positions:
            (map_pos_x, map_pos_y) = map_pos
            (x, y) = pos
            if x < 0:
                map_pos_x -= 1
            elif x > max_x:
                map_pos_x += 1
            elif y < 0:
                map_pos_y -= 1
            elif y > max_y:
                map_pos_y += 1
            if (map_pos_x, map_pos_y) in full_maps:
                continue
            for neighbor in map[(x % max_x, y % max_y)]:
                new_positions.add(((map_pos_x, map_pos_y), neighbor))
        positions = new_positions

        map_count = defaultdict(lambda: set())
        for map_pos, pos in positions:
            map_count[map_pos].add(pos)

        for map_pos in map_count.keys():
            if len(map_count[map_pos]) >= soils_per_map:
                full_maps.add(map_pos)

        if steps in [6, 10, 50, 100, 500, 1000, 5000]:
            print(steps, '->', len(positions) + (len(full_maps) * soils_per_map))

    return len(positions)


def main():
    examples = [
        ("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

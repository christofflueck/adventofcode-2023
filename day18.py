from run_util import run_puzzle


def parse_data(data: str):
    plan = []
    for row in data.split('\n'):
        direction, length, _ = row.split(' ')
        plan.append((direction, int(length)))
    return plan

def parse_data_b(data: str):
    plan = []
    for row in data.split('\n'):
        _, _, hex = row.split(' ')
        raw_hex = hex.replace('(#', '').replace(')', '')
        direction = None
        match raw_hex[-1]:
            case '0':
                direction = 'R'
            case '1':
                direction = 'D'
            case '2':
                direction = 'L'
            case '3':
                direction = 'U'
        plan.append((direction, int(raw_hex[:5], 16)))
    return plan


def part_a(data: str) -> int:
    data = parse_data(data)

    edges = []
    edge_start = (0, 0)

    distance_covered = 0

    for direction, length in data:
        edge_end = None
        match direction:
            case 'R':
                edge_end = (edge_start[0] + length, edge_start[1])
            case 'L':
                edge_end = (edge_start[0] - length, edge_start[1])
            case 'D':
                edge_end = (edge_start[0], edge_start[1] + length)
            case 'U':
                edge_end = (edge_start[0], edge_start[1] - length)
        distance_covered += length
        edges.append((edge_start, edge_end))
        edge_start = edge_end

    area = sum(
        [start[0] * end[1] - start[1] * end[0] for start, end in edges]
    )

    return area // 2 + distance_covered // 2 + 1


def part_b(data: str) -> int:
    data = parse_data_b(data)

    edges = []
    edge_start = (0, 0)

    distance_covered = 0

    for direction, length in data:
        edge_end = None
        match direction:
            case 'R':
                edge_end = (edge_start[0] + length, edge_start[1])
            case 'L':
                edge_end = (edge_start[0] - length, edge_start[1])
            case 'D':
                edge_end = (edge_start[0], edge_start[1] + length)
            case 'U':
                edge_end = (edge_start[0], edge_start[1] - length)
        distance_covered += length
        edges.append((edge_start, edge_end))
        edge_start = edge_end

    area = sum(
        [start[0] * end[1] - start[1] * end[0] for start, end in edges]
    )

    return area // 2 + distance_covered // 2 + 1


def main():
    examples = [
        ("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""", 62, 952408144115)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

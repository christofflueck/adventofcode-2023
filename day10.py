from typing import Tuple

from run_util import run_puzzle

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3


def go_up(coords: Tuple[int, int]):
    return (DOWN, (coords[0], coords[1] - 1))


def go_right(coords: Tuple[int, int]):
    return (LEFT, (coords[0] + 1, coords[1]))


def go_down(coords: Tuple[int, int]):
    return (UP, (coords[0], coords[1] + 1))


def go_left(coords: Tuple[int, int]):
    return (RIGHT, (coords[0] - 1, coords[1]))


def part_a(data: str) -> int:
    directions, starting_pos, tiles = parse_data(data)

    steps = 2
    while True:
        prev, curr = directions.pop(0)
        if curr not in tiles:
            raise Exception('Out of Bounds')
        next_tile = get_next_tile(curr, prev, tiles)
        steps += 1
        if any([x[1] == next_tile[1] for x in directions]):
            break
        directions.append(next_tile)
    return steps // 2


def get_next_tile(curr, prev, tiles):
    next_tile = None
    match tiles[curr]:
        case '|':
            if prev == UP:
                next_tile = go_down(curr)
            else:
                next_tile = go_up(curr)
        case '-':
            if prev == LEFT:
                next_tile = go_right(curr)
            else:
                next_tile = go_left(curr)
        case 'F':
            if prev == DOWN:
                next_tile = go_right(curr)
            else:
                next_tile = go_down(curr)
        case 'J':
            if prev == LEFT:
                next_tile = go_up(curr)
            else:
                next_tile = go_left(curr)
        case '7':
            if prev == LEFT:
                next_tile = go_down(curr)
            else:
                next_tile = go_left(curr)
        case 'L':
            if prev == RIGHT:
                next_tile = go_up(curr)
            else:
                next_tile = go_right(curr)
        case 'S':
            raise Exception('Got back to starting')
        case '.':
            raise Exception('Encountered Ground')
    return next_tile


def part_b(data: str) -> int:
    directions, starting_pos, tiles = parse_data(data)

    border = {starting_pos}
    left_of_border = set()
    right_of_border = set()
    prev, curr = directions.pop()

    while curr != starting_pos:
        if curr not in tiles:
            raise Exception('Out of Bounds')
        next_tile = get_next_tile(curr, prev, tiles)
        match tiles[curr]:
            case '-':
                if prev == LEFT:
                    #  L
                    # P-N
                    #  R
                    left_of_border.add(go_up(curr)[1])
                    right_of_border.add(go_down(curr)[1])
                else:
                    #  R
                    # N-P
                    #  L
                    left_of_border.add(go_down(curr)[1])
                    right_of_border.add(go_up(curr)[1])
            case '|':
                if prev == DOWN:
                    #  N
                    # L|R
                    #  P
                    left_of_border.add(go_left(curr)[1])
                    right_of_border.add(go_right(curr)[1])
                else:
                    #  P
                    # R|L
                    #  N
                    left_of_border.add(go_right(curr)[1])
                    right_of_border.add(go_left(curr)[1])
            case '7':
                if prev == DOWN:
                    #  RR
                    # N7R
                    #  P
                    right_of_border.add(go_right(curr)[1])
                    right_of_border.add(go_up(go_right(curr)[1])[1])
                    right_of_border.add(go_up(curr)[1])
                else:
                    #  LL
                    # P7L
                    #  N
                    left_of_border.add(go_right(curr)[1])
                    left_of_border.add(go_up(go_right(curr)[1])[1])
                    left_of_border.add(go_up(curr)[1])
            case 'J':
                if prev == UP:
                    #  P
                    # NJL
                    #  LL
                    left_of_border.add(go_right(curr)[1])
                    left_of_border.add(go_down(go_right(curr)[1])[1])
                    left_of_border.add(go_down(curr)[1])
                else:
                    #  N
                    # PJR
                    #  RR
                    right_of_border.add(go_right(curr)[1])
                    right_of_border.add(go_down(go_right(curr)[1])[1])
                    right_of_border.add(go_down(curr)[1])
            case 'F':
                if prev == DOWN:
                    # LL
                    # LFN
                    #  P
                    left_of_border.add(go_left(curr)[1])
                    left_of_border.add(go_up(go_left(curr)[1])[1])
                    left_of_border.add(go_up(curr)[1])
                else:
                    # RR
                    # RFN
                    #  P
                    right_of_border.add(go_left(curr)[1])
                    right_of_border.add(go_up(go_left(curr)[1])[1])
                    right_of_border.add(go_up(curr)[1])
            case 'L':
                if prev == UP:
                    #  P
                    # RLN
                    # RR
                    right_of_border.add(go_left(curr)[1])
                    right_of_border.add(go_down(go_left(curr)[1])[1])
                    right_of_border.add(go_down(curr)[1])
                else:
                    #  N
                    # LLP
                    # LL
                    left_of_border.add(go_left(curr)[1])
                    left_of_border.add(go_down(go_left(curr)[1])[1])
                    left_of_border.add(go_down(curr)[1])

        border.add(curr)

        prev, curr = next_tile

    for tile in border:
        if tile in left_of_border:
            left_of_border.remove(tile)
        if tile in right_of_border:
            right_of_border.remove(tile)

    smaller_dict = left_of_border if len(left_of_border) < len(right_of_border) else right_of_border
    larger_dict = left_of_border if len(left_of_border) > len(right_of_border) else right_of_border

    to_add = flood_area(border, smaller_dict)
    while len(to_add) > 0:
        smaller_dict = smaller_dict.union(to_add)
        to_add = flood_area(border, smaller_dict)

    for y in range(len(data.split('\n'))):
        print(''.join(
            [format_letter(smaller_dict, tiles, border, x, y) for x in
             range(len(data.split('\n')[0]))]))

    return len(smaller_dict)


def format_letter(smaller_dict, tiles, border, x, y):
    c = (x, y)
    if c in smaller_dict:
        return '\033[92mI\033[0m'
    if c in border:
        tile = tiles[c]
        match tile:
            case '7':
                tile = '┐'
            case 'J':
                tile = '┘'
            case 'F':
                tile = '┌'
            case 'L':
                tile = '└'

        return '\033[93m' + tile + '\033[0m'
    return '*'


def flood_area(border, smaller_dict):
    to_add = set()
    for pos in smaller_dict:
        neighbors = [go_up(pos)[1], go_left(pos)[1], go_right(pos)[1], go_down(pos)[1]]
        for neighbor in neighbors:
            if neighbor not in smaller_dict and neighbor not in border:
                to_add.add(neighbor)
    return to_add


def parse_data(data):
    rows = [x for x in data.split('\n')]
    tiles = dict()
    starting_pos = None
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            tiles[(x, y)] = cell
            if cell == 'S':
                starting_pos = (x, y)
    directions = []
    up = go_up(starting_pos)
    right = go_right(starting_pos)
    down = go_down(starting_pos)
    left = go_left(starting_pos)
    if up[1] in tiles and tiles[up[1]] in ['|', 'F', '7']:
        directions.append(up)
    if down[1] in tiles and tiles[down[1]] in ['|', 'J', 'L']:
        directions.append(down)
    if right[1] in tiles and tiles[right[1]] in ['-', '7', 'J']:
        directions.append(right)
    if left[1] in tiles and tiles[left[1]] in ['-', 'F', 'L']:
        directions.append(left)
    return directions, starting_pos, tiles


def main():
    examples = [
        (""".....
.S-7.
.|.|.
.L-J.
.....""", 4, None),
        ("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""", 4, None),
        ("""..F7.
.FJ|.
SJ.L7
|F--J
LJ...""", 8, None),
        ("""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""", 8, None),
        ("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""", None, 4),
        (""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""", None, 8),
        ("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""", None, 10),
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

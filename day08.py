import math

from run_util import run_puzzle
import re


def part_a(data: str) -> int:
    directions, left, right = parse_data(data)

    steps = 0
    curr = 'AAA'

    while curr != 'ZZZ':
        lookup = left if directions[steps % len(directions)] == 'L' else right
        curr = lookup[curr]
        steps += 1

    return steps


def parse_data(data: str):
    rows = [x for x in data.split('\n')]
    directions = rows[0]
    left = {}
    right = {}
    for row in rows[2:]:
        groups = re.search(r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", row)
        left[groups.group(1)] = groups.group(2)
        right[groups.group(1)] = groups.group(3)
    return directions, left, right


def part_b(data: str) -> int:
    directions, left, right = parse_data(data)

    current_nodes = set([key for key in left.keys() if key.endswith('A')] + [key for key in right.keys() if
                                                                         key.endswith('A')])

    steps = 0

    steps_to_end = []

    while len(current_nodes) > 0:
        next_nodes = []
        lookup = left if directions[steps % len(directions)] == 'L' else right
        steps += 1
        for node in current_nodes:
            next_node = lookup[node]
            if next_node.endswith('Z'):
                steps_to_end.append(steps)
            else:
                next_nodes.append(next_node)
        current_nodes = next_nodes

    return math.lcm(*steps_to_end)


def main():
    examples = [
        ("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""", 2, None),
        ("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""", 6, None
         ),
        ("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""", None, 6)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

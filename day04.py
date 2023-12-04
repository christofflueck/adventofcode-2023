from collections import deque
from typing import Set, Tuple

from run_util import run_puzzle
import re as re


def extract_row(row: str) -> Tuple[Set[int], Set[int]]:
    winning, card = row.split(': ')[1].split('| ')
    return (set([int(num) for num in winning.split(' ') if num.isnumeric()]),
            set([int(num) for num in card.split(' ') if num.isnumeric()])
            )


def card_matching(winning: Set[int], card: Set[int]):
    return len(winning.intersection(card))


def part_a(data):
    rows = [extract_row(x) for x in data.split('\n')]

    return sum([2 ** (card_matching(winning, card) - 1) for winning, card in rows if card_matching(winning, card) > 0])


def part_b(data):
    rows = [extract_row(x) for x in data.split('\n')]

    to_process = [1 for _ in rows]

    for index, value in enumerate(rows):
        winning, card = value
        matches = card_matching(winning, card)
        if matches == 0:
            continue
        for copy_index in range(matches):
            if len(to_process) > (index + copy_index + 1):
                to_process[index + copy_index + 1] += to_process[index]

    return sum(to_process)


def main():
    examples = [
        ("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""", 13, 30)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

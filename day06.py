import math
import re as re
from typing import List, Tuple
from tqdm import tqdm

from run_util import run_puzzle


def part_a(data: str):
    races = parse_races(data)

    leeways = get_number_of_winning_races(races)

    return math.prod(leeways)


def get_number_of_winning_races(races):
    leeways = []
    for time, distance in races:
        possible = 0
        for windup_and_speed in range(1, time - 1):
            max_distance = (time - windup_and_speed) * windup_and_speed
            if max_distance > distance:
                possible += 1
        leeways.append(possible)
    return leeways


def parse_races(data: str) -> List[Tuple[int, int]]:
    times, distances = [[int(n) for n in re.split('\\s', row) if n.isnumeric()] for row in data.split('\n')]
    races = list(zip(times, distances))
    return races


def part_b(data: str):
    times, distances = [int(''.join(re.search('(\\d+)', row.replace(' ', '')).groups())) for row in data.split('\n')]

    leeways = get_number_of_winning_races([(times, distances)])
    return sum(leeways)


def main():
    examples = [
        ("""Time:      7  15   30
Distance:  9  40  200""", 288, 71503)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

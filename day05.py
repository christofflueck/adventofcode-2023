from typing import List, Tuple

from run_util import run_puzzle
from tqdm import tqdm


def parse_lookups(rows):
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    row_num = 2
    row_num = extract_next_rows(row_num, rows, seed_to_soil)
    row_num = extract_next_rows(row_num, rows, soil_to_fertilizer)
    row_num = extract_next_rows(row_num, rows, fertilizer_to_water)
    row_num = extract_next_rows(row_num, rows, water_to_light)
    row_num = extract_next_rows(row_num, rows, light_to_temperature)
    row_num = extract_next_rows(row_num, rows, temperature_to_humidity)
    extract_next_rows(row_num, rows, humidity_to_location)

    # Sort the data so the ranges don't need to be searched multiple times but can be done in sequence
    lookups = [
        sorted(seed_to_soil),
        sorted(soil_to_fertilizer),
        sorted(fertilizer_to_water),
        sorted(water_to_light),
        sorted(light_to_temperature),
        sorted(temperature_to_humidity),
        sorted(humidity_to_location),
    ]
    return lookups


def extract_next_rows(row_num, rows, range_map):
    while row_num < len(rows) and rows[row_num][0].isnumeric():
        dest_start, source_start, range_len = [int(x) for x in rows[row_num].split(' ')]
        range_map.append((source_start, source_start + range_len, dest_start - source_start))
        row_num += 1

    return row_num + 1


def part_a(data):
    rows = [row for row in data.split('\n') if row != '']
    seeds = [(int(x), int(x)) for x in rows[0].split(': ')[1].split(' ')]
    lookups = parse_lookups(rows)

    locations = get_seed_location(lookups, seeds)

    return min([x[0] for x in locations])


def get_seed_location(lookups, seeds: List[Tuple[int, int]]):
    out = []
    current = seeds
    # iterate over all lookups
    for lookup in lookups:
        resolved = []
        # We will have multiple ranges so we iterate them one by one
        while len(current) > 0:
            seed_start, seed_end = current.pop()
            # For each mapping in that conversion
            for src_start, src_end, diff in lookup:
                # Fully in range
                if src_start <= seed_start and seed_end <= src_end:
                    resolved.append((seed_start + diff, seed_end + diff))
                    seed_start = 0
                    seed_end = 0
                    break

                # overlapping start
                if src_start <= seed_start < src_end < seed_end:
                    resolved.append((seed_start + diff, src_end + diff))
                    seed_start = src_end
                    current.append((seed_start, seed_end))

                # seed envelops the range
                if seed_start < src_start < src_end < seed_end:
                    resolved.append((src_start + diff, seed_end + diff))
                    seed_end = src_start - 1
                    current.append((seed_start, seed_end))

                # I feel like I'm missing a case here seed_start < src_start < seed_end <= seed_start but it works

            # fallback for no mapping available
            if seed_start > 0 and seed_end > 0:
                resolved.append((seed_start, seed_end))

        # Provide the current solutions to the next lookup or the output
        current = resolved

    return current


def part_b(data):
    rows = [row for row in data.split('\n') if row != '']
    seed_range_def = [int(x) for x in rows[0].split(': ')[1].split(' ')]
    seed_ranges = [(seed_range_def[i], seed_range_def[i] + seed_range_def[i + 1] - 1) for i in
                   range(0, len(seed_range_def), 2)]

    lookups = parse_lookups(rows)

    locations = get_seed_location(lookups, seed_ranges)

    range_starts = [x[0] for x in locations]
    return min(range_starts)


def main():
    examples = [
        ("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""", 35, 46)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

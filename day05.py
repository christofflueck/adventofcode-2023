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
    lookups = [
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
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
    seeds = [int(x) for x in rows[0].split(': ')[1].split(' ')]
    lookups = parse_lookups(rows)

    locations = []

    for seed in seeds:
        locations.append(get_seed_location(lookups, seed))

    return min(locations)


def get_seed_location(lookups, seed):
    curr_num = seed
    for lookup in lookups:
        for src_start, src_end, dest in lookup:
            if src_start <= curr_num <= src_end:
                curr_num += dest
                break
    return curr_num


def part_b(data):
    rows = [row for row in data.split('\n') if row != '']
    seed_range_def = [int(x) for x in rows[0].split(': ')[1].split(' ')]
    seed_ranges = []
    for i in range(len(seed_range_def) // 2):
        seed_ranges.append(range(seed_range_def[i * 2], seed_range_def[i * 2] + seed_range_def[(i * 2) + 1]))

    lookups = parse_lookups(rows)

    locations = []

    for seed_range in tqdm(seed_ranges, 'ranges'):
        for seed in tqdm(seed_range, 'current range'):
            locations.append(get_seed_location(lookups, seed))

    return min(locations)


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

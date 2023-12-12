from run_util import run_puzzle


def parse_data(data: str):
    rows = data.split(' ')
    nums = [[int(x) for x in row[1].split(',')] for row in rows]
    springs = [row[0] for row in rows]
    return zip(springs, nums)


def part_a(data: str) -> int:
    rows = parse_data(data)

    arrangements = []

    for spring, nums in rows:



    return 0


def part_b(data: str) -> int:
    data = parse_data(data)
    return 0


def main():
    examples = [
        ("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 21, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

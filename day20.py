from run_util import run_puzzle


def parse_data(data: str):
    modules = {}
    for row in data.split('\n'):
        module, targets = row.split(' -> ')
        type = None
        if '&' in module or '%' in module:
            type = row[:1]
            module = module[1:]
        targets = targets.split(', ')
        modules[module] = (type, targets)
    return modules

# & -> when all inputs are high -> send low
# % -> high pulse -> ignored, low pulse -> toggle
def part_a(data: str) -> int:
    modules = parse_data(data)
    return 0


def part_b(data: str) -> int:
    data = parse_data(data)
    return 0


def main():
    examples = [
        ("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 32000000, 1),
        ("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""", 11687500, 1),
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

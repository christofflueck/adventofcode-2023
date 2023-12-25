from collections import defaultdict

from run_util import run_puzzle

# Found these through Graph Visualization

TO_BE_CUT = [
    ['dhl', 'vfs'],
    ['nzn', 'pbq'],
    ['zpc', 'xvp'],
]


def parse_data(data: str):
    components = defaultdict(lambda: list())
    for row in data.splitlines():
        component, rest = row.split(': ')
        linked = rest.split(' ')
        for c in linked:
            is_blocked = False
            for blocked in TO_BE_CUT:
                if c in blocked and component in blocked:
                    is_blocked = True

            if not is_blocked:
                components[component].append(c)
                components[c].append(component)

    return components


def part_a(data: str) -> int:
    components = parse_data(data)
    left = {'dhl', 'nzn', 'zpc'}
    right = {'vfs', 'pbq', 'xvp'}

    f = open("day25.dot", "w")
    f.write("graph {")
    for key in components.keys():
        for target in components[key]:
            f.write(f"    {key} -- {target};")
    f.write("}")
    f.close()
    to_be_added = set(components.keys()) - left - right

    while to_be_added:
        for key in left.copy():
            left.update(components[key])
        for key in right.copy():
            right.update(components[key])

        to_be_added = set(components.keys()) - left - right

    return len(left) * len(right)


def part_b(data: str) -> int:
    data = parse_data(data)
    return 0


def main():
    examples = [
        ("""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""", None, 1)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

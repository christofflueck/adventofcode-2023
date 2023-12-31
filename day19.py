import re

from run_util import run_puzzle


def parse_data(data: str):
    workflow_strings, part_strings = [section.split('\n') for section in data.split('\n\n')]

    workflows = {}
    for row in workflow_strings:
        name, rest = row.replace('}', '').split('{')
        workflows[name] = list()
        actions = rest.split(',')
        for action in actions:
            if ':' in action:
                prop, action, val, target = re.search("([a-zA-Z]+)([<>])([0-9]+):([a-zA-Z]+)", action).groups()
                workflows[name].append((prop, action, int(val), target))
            else:
                workflows[name].append(action)

    parts = []
    for part in part_strings:
        x, m, a, s = [re.search("([0-9]+)", val).group(0) for val in part.split(',')]
        parts.append({
            "x": int(x),
            "m": int(m),
            "a": int(a),
            "s": int(s)
        })

    return workflows, parts


def run_workflows(part, workflows):
    next_workflow = "in"
    while next_workflow:
        if next_workflow == 'A':
            return True
        if next_workflow == 'R':
            return False
        workflow = workflows[next_workflow]
        for test in workflow:
            if isinstance(test, str):
                next_workflow = test
                break
            prop, check, value, target = test
            if (check == '>' and part[prop] > value) or (check == '<' and part[prop] < value):
                next_workflow = target
                break


def part_a(data: str) -> int:
    workflows, parts = parse_data(data)

    accepted = []

    for part in parts:
        if run_workflows(part, workflows):
            accepted.append(part)

    return sum([sum(part.values()) for part in accepted])


def part_b(data: str) -> int:
    workflows, parts = parse_data(data)

    accepted = []
    all_parts = [({
                      "x": (1, 4000),
                      "m": (1, 4000),
                      "a": (1, 4000),
                      "s": (1, 4000),
                  }, "in")]

    while all_parts:
        part, next_workflow = all_parts.pop()
        if next_workflow == 'A':
            accepted.append(part)
            continue
        if next_workflow == 'R':
            continue
        workflow = workflows[next_workflow]
        for test in workflow:
            if isinstance(test, str):
                all_parts.append((part, test))
                break
            prop, check, value, target = test
            part_min, part_max = part[prop]
            if part_min <= value < part_max:
                true_part = part.copy()
                false_part = part.copy()
                if check == '>':
                    true_part[prop] = (value + 1, part_max)
                    false_part[prop] = (part_min, value)
                else:
                    true_part[prop] = (part_min, value - 1)
                    false_part[prop] = (value, part_max)
                part = false_part
                all_parts.append((true_part, target))
                continue
            if value <= part_min:
                if check == '>':
                    all_parts.append((part, target))
                    break
                else:
                    continue
            if value >= part_max:
                if check == '<':
                    all_parts.append((part, target))
                    break
                else:
                    continue
    accepted_parts_sum = 0
    for part in accepted:
        accepted_parts_val = 1
        for part_min, part_max in part.values():
            accepted_parts_val *= part_max - part_min + 1
        accepted_parts_sum += accepted_parts_val
    return accepted_parts_sum


def main():
    examples = [
        ("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""", 19114, 167409079868000)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

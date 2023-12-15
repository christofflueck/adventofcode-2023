import re

from run_util import run_puzzle


def holiday_ascii(string: str) -> int:
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256
    return val


def parse_data(data: str):
    return data.replace('\n', '').split(',')


def parse_data_b(data: str):
    actions = []
    for word in parse_data(data):
        if '=' in word:
            lens, val = word.split('=')
            actions.append((lens, '=', int(val)))
        else:
            actions.append((word[:-1], '-', None))

    return actions


def part_a(data: str) -> int:
    data = parse_data(data)

    return sum([holiday_ascii(word) for word in data])


def part_b(data: str) -> int:
    data = parse_data_b(data)

    boxes = [{} for _ in range(256)]

    for lens, operation, val in data:
        box_index = holiday_ascii(lens)
        box = boxes[box_index]

        if operation == '-':
            box.pop(lens, None)
        else:
            box[lens] = val

    lens_powers = []
    for box_power, box in enumerate(boxes):
        for slot, key in enumerate(box.keys()):
            lens_powers.append(box[key] * (slot + 1) * (box_power + 1))

    return sum(lens_powers)


def main():
    assert holiday_ascii('HASH') == 52
    examples = [
        ("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""", 1320, 145)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

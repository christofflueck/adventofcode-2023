from run_util import run_puzzle
import json


def parse_data(data: str):
    modules = {}
    for row in data.split('\n'):
        module, targets = row.split(' -> ')
        type = None
        if '&' in module or '%' in module:
            type = row[:1]
            module = module[1:]
        targets = targets.split(', ')
        if type == '%':
            modules[module] = (type, targets, False)
        elif type == '&':
            modules[module] = (type, targets, {})
        else:
            modules[module] = (type, targets, None)
    modules['output'] = (None, [], None)
    modules['rx'] = (None, [], {False: 0, True: 0})
    for module in modules.keys():
        for target in modules[module][1]:
            if modules[target][0] == '&':
                modules[target][2][module] = False
    return modules


# & -> when all inputs are high -> send low
# % -> high pulse -> ignored, low pulse -> toggle
def part_a(data: str) -> int:
    modules = parse_data(data)
    next_moves = [('broadcaster', False, 'button')]  # target, high, source
    initial_state = json.dumps(modules)

    button_presses = 1
    low_pulses_sent = 0
    high_pulses_sent = 0
    while next_moves and button_presses <= 1000:
        target_key, high, source_key = next_moves.pop(0)
        if high:
            high_pulses_sent += 1
        else:
            low_pulses_sent += 1

        target = modules[target_key]
        type, next_targets, state = target

        if type is None:
            for next_target in next_targets:
                next_moves.append((next_target, False, target_key))
        elif type == '%':
            if not high:
                modules[target_key] = (type, next_targets, not state)
                for next_target in next_targets:
                    next_moves.append((next_target, not state, target_key))
        elif type == '&':
            state[source_key] = high
            for next_target in next_targets:
                next_moves.append((next_target, not all(state.values()), target_key))

        if not next_moves:
            current_state = json.dumps(modules)
            if current_state != initial_state:
                next_moves.append(('broadcaster', False, 'button'))
                button_presses += 1

    cycles = 1000 // min(button_presses, 1000)
    return cycles ** 2 * high_pulses_sent * low_pulses_sent


def part_b(data: str) -> int:
    modules = parse_data(data)

    next_moves = [('broadcaster', False, 'button')]  # target, high, source
    initial_state = json.dumps(modules)
    states = []
    # print('button False -> broadcaster')
    button_presses = 1

    # print('starting')
    while next_moves:
        target_key, high, source_key = next_moves.pop(0)
        target = modules[target_key]
        type, next_targets, state = target

        if target_key == 'rx':
            state[high] += 1
        elif type is None:
            print(target_key, False, '->', ", ".join(next_targets))
            for next_target in next_targets:
                next_moves.append((next_target, False, target_key))
        elif type == '%':
            if not high:
                modules[target_key] = (type, next_targets, not state)
                print(target_key, not state, '->', ", ".join(next_targets))
                for next_target in next_targets:
                    next_moves.append((next_target, not state, target_key))
            else:
                print(target_key, ' not high')
        elif type == '&':
            state[source_key] = high
            print(target_key, not all(state.values()), '->', ", ".join(next_targets))
            for next_target in next_targets:
                next_moves.append((next_target, not all(state.values()), target_key))

        if not next_moves:
            current_state = json.dumps(modules)
            if current_state in states:
                print('LOOP DETECTED', button_presses, 'prev', states.index(current_state))
                break
            if modules['rx'][2][True] != 0 or modules['rx'][2][False] != 1:
                print('rx received', modules['rx'][2], 'signals', button_presses)
                button_presses += 1
                next_moves.append(('broadcaster', False, 'button'))
                modules['rx'][2][True] = 0
                modules['rx'][2][False] = 0
            else:
                print('rx received', modules['rx'][2], 'signals')

    return button_presses


def main():
    examples = [
        ("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 32000000, None),
        ("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx""", 11687500, None),
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()

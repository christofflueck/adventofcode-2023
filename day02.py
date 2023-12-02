from run_util import run_puzzle


def part_a(data:str):
    games = get_games(data)

    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14

    game_nos = [g['no'] for g in games if g["red"] <= MAX_RED and g['green'] <= MAX_GREEN and g['blue'] <= MAX_BLUE]
    return sum(game_nos)


def get_games(data):
    rows = [row.split(': ') for row in data.split('\n')]
    games = []
    for [gamestr, colors] in rows:
        gameno = int(gamestr.split(' ')[1])
        game = {
            "no": gameno,
            "red": 0,
            "blue": 0,
            "green": 0
        }
        for stage in colors.split('; '):
            stagecolors = {
                "red": 0,
                "blue": 0,
                "green": 0
            }
            for hand in stage.split(', '):
                [num, color] = hand.split(' ')
                num = int(num)
                stagecolors[color] = stagecolors[color] + num

            for color in stagecolors.keys():
                game[color] = max(game[color], stagecolors[color])
        games.append(game)
    return games


def part_b(data):
    games = get_games(data)
    return sum([ g["red"] * g["blue"] * g["green"] for g in games])


def main():
    examples = [
        ("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", 8, 2286)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
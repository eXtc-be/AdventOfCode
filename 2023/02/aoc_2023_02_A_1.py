# aoc_2023_02_A_1.py - Day 2: Cube Conundrum - part 1
# Determine which games would have been possible if the bag had been loaded with only 12 red cubes,
# 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
# https://adventofcode.com/2023/day/2


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_02'

COLORS = {'red': 12, 'green': 13, 'blue': 14}  # serves as list of possible colors AND for checking games


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_games(data_lines: list[str]) -> dict[int, list[dict[str, int]]]:
    games = {}

    for line in data_lines:
        game_id, rest = line.split(':')
        game_id = int(game_id.split()[-1])

        games[game_id] = []

        for subset in rest.split('; '):
            cubes = {}
            for cube in subset.split(', '):
                number, color = cube.strip().split(' ')
                cubes[color.lower()] = int(number)

            # add missing colors from bag
            for color in COLORS:
                if color not in cubes:
                    cubes[color] = 0

            games[game_id].append(cubes)

    return games


def analyze_games(games: dict[int, list[dict[str, int]]]) -> dict[int, dict[str, int]]:
    summary = {}

    for game_id, values in games.items():
        cubes = {}
        for color in COLORS:
            cubes[color] = max(subset[color] for subset in values)
        summary[game_id] = cubes

    return summary


def find_possible_games(summary: dict[int, dict[str, int]]) -> list[int]:
    result = []

    for game_id, cubes in summary.items():
        if all(cubes[color] <= value for color, value in COLORS.items()):
            result.append(game_id)

    return result


test_data = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    games = get_games(data_lines)
    # pprint(games)

    summary = analyze_games(games)
    # pprint(summary)

    possible_games = find_possible_games(summary)
    # print(possible_games)

    print(f'End result: {sum(possible_games)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 8
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 3059
    #   Finished 'main' in 1 millisecond

# aoc_2023_02_A_1.py - Day 2: Cube Conundrum - part 1
# test if certain cube combinations are possible
# https://adventofcode.com/2023/day/2


# imports


DATA_PATH = './input_2023_02'

colors = {'red': 12, 'green': 13, 'blue': 14}  # serves as list of possible colors AND for checking games


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def split_data(lines):
    result = {}
    for line in lines:
        id_, rest = line.split(':')
        id_ = int(id_.lower().replace('game ', ''))
        result[id_] = []
        subsets = rest.split('; ')
        for subset in subsets:
            cubes = subset.split(', ')
            set_ = {}
            for cube in cubes:
                number, color = cube.strip().split(' ')
                set_[color.lower()] = int(number)
            for color in colors:
                if color not in set_:
                    set_[color] = 0
            result[id_].append(set_)
    return result


def summarize_data(data):
    result = {}
    for id_, values in data.items():
        color_values = {}
        for color in colors:
            color_values[color] = max(subset[color] for subset in values)
        result[id_] = color_values
    return result


def get_possible_games(summary):
    result = []
    for id_, color_values in summary.items():
        if all(color_values[color] <= value for color, value in colors.items()):
            result.append(id_)
    return result


test_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    data = split_data(data_lines)
    print(data)

    summary = summarize_data(data)
    print(summary)

    possible_games = get_possible_games(summary)
    print(possible_games)

    print(f'End result: {sum(possible_games)}')

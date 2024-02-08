# aoc_2016_01_A_1.py - Day 1: No Time for a Taxicab - part 1
# How many blocks away is Easter Bunny HQ?
# https://adventofcode.com/2016/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2016_01'

HEADINGS = {
    'N': {'L': 'W', 'R': 'E', 'friendly': 'norht'},
    'E': {'L': 'N', 'R': 'S', 'friendly': 'east'},
    'S': {'L': 'E', 'R': 'W', 'friendly': 'west'},
    'W': {'L': 'S', 'R': 'N', 'friendly': 'south'},
}

TURNS = {
    'L': 'left',
    'R': 'right',
}

DIRECTIONS = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_directions(direction_string: str) -> list[str]:
    return direction_string.split(', ')


test_data = '''
R2, L3
R2, R2, R2
R5, L5, R5, R3
'''.strip().splitlines()


@time_it
def main(direction_string: str) -> None:
    directions = get_directions(direction_string)
    # pprint(directions)

    current_heading = 'N'
    current_position = [0, 0]

    for direction in directions:
        turn, blocks = direction[0], int(direction[1:])
        current_heading = HEADINGS[current_heading][turn]
        print(f'turning {TURNS[turn]} heading {HEADINGS[current_heading]["friendly"]} moving {blocks} blocks ', end='')
        current_position[0] += DIRECTIONS[current_heading][0] * blocks
        current_position[1] += DIRECTIONS[current_heading][1] * blocks
        print(f'to position {current_position}')

    print(f'\nFinal position: {current_position}')

    print(f'\nDistance from start: {sum(abs(axis) for axis in current_position)}')


if __name__ == "__main__":
    data_line = load_data(DATA_PATH)[0]
    # data_line = test_data[0]
    # data_line = test_data[1]
    # data_line = test_data[2]
    # print(data_line)

    main(data_line)
    # using test_data 1:
    #   End result: 5
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using test_data 3:
    #   End result: 12
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 146
    #   Finished 'main' in 3 milliseconds

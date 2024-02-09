# aoc_2016_01_A_1.py - Day 1: No Time for a Taxicab - part 1
# How many blocks away is Easter Bunny HQ?
# https://adventofcode.com/2016/day/1


from tools import time_it

from dataclasses import dataclass

from pprint import pprint

@dataclass
class Coordinates:
    x: int
    y: int

    def distance(self, origin: 'Coordinates' = None) -> int:
        origin = Coordinates(0, 0) if origin is None else origin
        return abs(self.x - origin.x) + abs(self.y - origin.y)

    def __str__(self):
        return f'({self.x}, {self.y})'


DATA_PATH = './input_2016_01'

HEADINGS = {
    'N': {'L': 'W', 'R': 'E', 'friendly': 'norht'},
    'E': {'L': 'N', 'R': 'S', 'friendly': 'east'},
    'S': {'L': 'E', 'R': 'W', 'friendly': 'south'},
    'W': {'L': 'S', 'R': 'N', 'friendly': 'west'},
}

TURNS = {
    'L': 'left',
    'R': 'right',
}

DIRECTIONS = {
    'N': Coordinates(0, 1),
    'E': Coordinates(1, 0),
    'S': Coordinates(0, -1),
    'W': Coordinates(-1, 0),
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
    current_position = Coordinates(0, 0)

    for direction in directions:
        turn, blocks = direction[0], int(direction[1:])
        current_heading = HEADINGS[current_heading][turn]
        print(f'turning {TURNS[turn]} heading {HEADINGS[current_heading]["friendly"]} moving {blocks} blocks ', end='')
        current_position.x += DIRECTIONS[current_heading].x * blocks
        current_position.y += DIRECTIONS[current_heading].y * blocks
        print(f'to position {current_position}')

    print(f'\nEaster Bunny Headquarters position: {current_position}')

    print(f'Distance from start: {current_position.distance()}\n')


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

    # test Coordinates.distance()
    # coord = Coordinates(10, 10)
    # print(coord, coord.distance())
    # print(coord, coord.distance(Coordinates(5, 5)))

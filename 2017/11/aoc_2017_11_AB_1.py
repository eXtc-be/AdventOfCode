# aoc_2017_11_AB_1.py - Day 11: Hex Ed - part 1
# You have the path the child process took.
# Starting where he started, you need to determine the fewest number of steps required to reach him.
# How many steps away is the furthest he ever got from his starting position?
# https://adventofcode.com/2017/day/11


from tools import time_it

from typing import NamedTuple

from pprint import pprint


DATA_PATH = './input_2017_11'


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def distance(self, other: 'Point') -> int:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        return dx + max(0, (dy - dx) // 2)


DIRECTIONS = {
    'n': Point(0, 2),
    's': Point(0, -2),
    'nw': Point(-1, 1),
    'ne': Point(1, 1),
    'sw': Point(-1, -1),
    'se': Point(1, -1),
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_instructions(data: str) -> list[str]:
    return data.split(',')


def follow_instructions(instructions: list[str]) -> tuple[int, int]:
    current_position = origin = Point(0, 0)
    furthest = 0

    for instruction in instructions:
        current_position += DIRECTIONS[instruction]
        furthest = max(furthest, current_position.distance(origin))

    return current_position.distance(Point(0, 0)), furthest


test_data = '''
ne,ne,ne
ne,ne,sw,sw
ne,ne,s,s
se,sw,se,sw,sw
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    instructions = get_instructions(data)
    # print(instructions)

    current_distance, furthest_distance = follow_instructions(instructions)

    print(f'End result: {current_distance, furthest_distance}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # for line in data_lines:
    #     main(line)
    # using test_data:
    #   End result: (3, 3), (0, 2), (2, 2), (3, 3)
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: (812, 1603)
    #   Finished 'main' in 15 milliseconds

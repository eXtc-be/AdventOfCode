# aoc_2016_02_A_1.py - Day 2: Bathroom Security - part 1
# What is the bathroom code?
# https://adventofcode.com/2016/day/2


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


DATA_PATH = './input_2016_02'

KEYPAD = """
1 2 3
4 5 6
7 8 9
"""

DIRECTIONS = {
    'U': Coordinates(0, -1),
    'R': Coordinates(1, 0),
    'D': Coordinates(0, 1),
    'L': Coordinates(-1, 0),
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_instructions(datalines: list[str]) -> list[list[str]]:
    return [[c for c in line] for line in datalines]


def get_keypad() -> list[list[str]]:
    return [[c for c in line.strip().split()] for line in KEYPAD.splitlines() if line]


test_data = '''
ULL
RRDDD
LURDL
UUUUD
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    instructions = get_instructions(data_lines)
    # pprint(instructions)

    keypad = get_keypad()
    # pprint(keypad)

    code = ''
    min_row, max_row = 0, len(keypad) - 1
    min_col, max_col = 0, len(keypad[0]) - 1
    pos = Coordinates(1, 1)  # start position ('5')

    for line in instructions:
        for instruction in line:
            pos.x += DIRECTIONS[instruction].x
            pos.x = max(min_col, min(max_col, pos.x))
            pos.y += DIRECTIONS[instruction].y
            pos.y = max(min_row, min(max_row, pos.y))
        code += keypad[pos.y][pos.x]

    print(f'End result: {code}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 1985
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 69642
    #   Finished 'main' in 3 milliseconds

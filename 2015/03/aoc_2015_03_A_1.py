# aoc_2015_03_A_1.py - Day 3: Perfectly Spherical Houses in a Vacuum - part 1
# How many houses receive at least one present from Santa?
# https://adventofcode.com/2015/day/3


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_03'

DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def find_houses(instructions: str) -> set[tuple[int, int]]:
    houses = {(0, 0)}
    row, col = 0, 0

    for instruction in instructions:
        row, col = tuple(map(lambda a, b: a + b,(row, col), DIRECTIONS[instruction]))
        houses.add((row, col))

    return houses


test_data = '''
>
^>v<
^v^v^v^v^v
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, find_houses(line))

    houses = find_houses(data_lines[0])

    print(f'End result: {len(houses)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 2081
    #   Finished 'main' in 8 milliseconds

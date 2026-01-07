# aoc_2025_04_A_1.py - Day 4: Printing Department - part 1
# Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?
# https://adventofcode.com/2025/day/4

from tools import time_it

# other imports

from pprint import pprint
from collections import namedtuple


DATA_PATH = './input_2025_04'

# other constants
Coord = namedtuple('Coord', ['x', 'y'])

DIRECTIONS = [
    Coord(-1, -1), Coord(0, -1), Coord(1, -1),
    Coord(-1,  0),               Coord(1,  0),
    Coord(-1,  1), Coord(0,  1), Coord(1,  1),
]


# classes


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def count_adjacent(grid: list[list[str]], coord: Coord) -> int:
    result = 0

    for direction in DIRECTIONS:
        if 0 <= coord.x + direction.x < len(grid[0]) and 0 <= coord.y + direction.y < len(grid):
            result += 1 if grid[coord.y + direction.y][coord.x + direction.x] == '@' else 0

    return result


test_data = '''
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    grid = [[char for char in line] for line in data_lines]

    result = sum(
        1 if count_adjacent(grid, Coord(col, row)) < 4 and grid[row][col] == '@' else 0
        for row in range(len(grid))
        for col in range(len(grid[row]))
    )

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 13
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1372
    #   Finished 'main' in 60 milliseconds

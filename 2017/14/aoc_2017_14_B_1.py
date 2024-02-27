# aoc_2017_14_B_1.py - Day 14: Disk Defragmentation - part 2
# How many regions are present given your key string?
# https://adventofcode.com/2017/day/14


from aoc_2017_14_A_1 import (
    DATA_PATH,
    HEX_TO_BITS,
    load_data,
    test_data,
    knothash,
)

from tools import time_it

# other imports

from pprint import pprint


DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]

USED = '#'
FREE = '.'

ROWS_TEST = 8
COLS_TEST = 8

ROWS = 128
COLS = 128


def calc_grid(data_lines: list[str], rows: int = ROWS, cols: int = COLS) -> list[str]:
    grid = []

    for i in range(rows):
        hex_hash = knothash(data_lines[0] + f'-{i}')
        grid.append(''.join(HEX_TO_BITS[c] for c in hex_hash[:cols//4]))

    return grid


def _fill_region(grid: list[str], numbers: list[list[int]], r: int, c: int, group: int) -> None:
    for d in DIRECTIONS:
        if 0 <= r+d[0] < len(grid) and 0 <= c+d[1] < len(grid[r]):
            if grid[r+d[0]][c+d[1]] == USED and numbers[r+d[0]][c+d[1]] == 0:
                numbers[r+d[0]][c+d[1]] = group
                _fill_region(grid, numbers, r+d[0], c+d[1], group)


def find_groups(grid: list[str], numbers: list[list[int]]) -> int:
    group = 0

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == USED and numbers[r][c] == 0:
                group += 1
                numbers[r][c] = group
                _fill_region(grid, numbers, r, c, group)

    return group


@time_it
def main(data_lines: list[str], rows: int = ROWS, cols: int = COLS) -> None:
    grid = calc_grid(data_lines, rows, cols)
    # print('\n'.join(grid))

    # print('-' * 100)

    numbers = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    groups = find_groups(grid, numbers)
    # print('\n'.join(''.join(f'{num:03} ' if num else '    ' for num in row) for row in numbers))

    print(f'End result: {groups}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    # main(data_lines)
    main(data_lines, ROWS_TEST, COLS_TEST)
    # using test_data:
    #   End result: 12
    #   Finished 'main' in 98 milliseconds
    # using input data:
    #   End result: 1018
    #   Finished 'main' in 1.62 seconds

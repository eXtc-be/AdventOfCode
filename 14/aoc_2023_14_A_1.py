# aoc_2023_14_A_1.py - Day 14: Parabolic Reflector Dish - part 1
# Tilt the platform so that the rounded rocks all roll north.
# Afterward, what is the total load on the north support beams?
# https://adventofcode.com/2023/day/14


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_14'

ROUND_ROCK = 'O'
CUBE_ROCK = '#'
EMPTY = '.'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_grid(data_lines: list[str]) -> list[list[str]]:
    return [[char for char in line] for line in data_lines]


def _slide_rock(grid: list[list[str]], row: int, col: int) -> None:
    for r in range(row -1, -1, -1):  # count down from row to zero
        if grid[r][col] == EMPTY:
            grid[r][col] = grid[r+1][col]  # copy rock in current cell to row below
            grid[r + 1][col] = EMPTY  # mark current cell as empty
        else:
            # if CUBE_ROCK: keeps ROUND_ROCKs from falling any further
            # if ROUND_ROCK: rows 'below' this one are filled with ROUND_ROCKs or there is a CUBE_ROCK somewhere
            break


def tilt_grid(grid: list[list[str]]) -> list[list[str]]:
    tilted_grid = [[cell for cell in line] for line in grid]  # copy grid
    for r, row in enumerate(grid[1:], 1):  # skip first row
        for c, char in enumerate(row):
            if char == ROUND_ROCK:
                _slide_rock(tilted_grid, r, c)

    return tilted_grid


def calc_load(grid: list[list[str]]) -> list[int]:
    load = []
    for factor, row in enumerate(grid, -len(grid)):
        load.append(-factor * row.count(ROUND_ROCK))

    return load


# test_data = """
# .....
# #O#.#
# .....
# OO.O.
# """.strip().splitlines()


test_data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # pprint(grid)

    # print('-' * 100)

    tilted_grid = tilt_grid(grid)
    # pprint(tilted_grid)

    load = calc_load(tilted_grid)
    # print(load)

    print(f'End result: {sum(load)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 136
    #   Finished 'main' in 0 milliseconds
    # using input data:
    #   End result: 107053
    #   Finished 'main' in 3 milliseconds

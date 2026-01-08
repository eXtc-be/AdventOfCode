# aoc_2023_10_B_2.py - Day 10: Pipe Maze - part 2
# How many tiles are enclosed by the loop?
# https://adventofcode.com/2023/day/10
# new tactic: for each and every cell check if we can reach one of the sides without touching the loop
# I got this working, except for grids where you have to 'squeeze' between pipes
# I can't figure out how to implement that


from aoc_2023_10_A_1 import (
    DATA_PATH,
    load_data,
    # test_data_1,
    # test_data_2,
    create_grid,
    find_start,
    find_loop,
    START,
    PIPES,
    DIRECTIONS,
)

from aoc_2023_10_B_1 import (
    replace_start,
    test_data_1,
    test_data_1a,
    test_data_1b,
    test_data_1c,
    test_data_1d,
    test_data_1e,
    test_data_1f,
    test_data_1g,
    test_data_1h,
    test_data_2a,
    test_data_2b,
    test_data_3,
    test_data_4,
    test_data_4b,
    test_data_4b,
    test_data_5,
    test_data_5a,
    test_data_5b,
    test_data_5c,
    test_data_6,
    test_data_7,
)

from tools import time_it

from enum import Enum, auto

from pprint import pprint


class Found(Enum):
    NOTHING = auto()
    EMPTY = auto()
    LOOP = auto()
    EDGE = auto()


# INSIDE = '●'
# INSIDE = '■'
INSIDE = '█'
# INSIDE = '░'
# INSIDE = '▒'
# INSIDE = '▓'

PIPE_TO_BOX = {
    START: START,
    '|': '│',
    '-': '─',
    'L': '└',
    'J': '┘',
    'F': '┌',
    '7': '┐',
    '.': '░',
    Found.LOOP: INSIDE,
    INSIDE: INSIDE,
}


def _find_edge(
        grid: list[list[str]],
        loop: list[tuple[int, int]],
        row: int,
        col: int,
        visited: list[tuple[int, int]] = []
):
    """
    starting at row, col, tries to get to the edge of the grid
    without touching the loop (except for squeezing between 2 parallel pipes)
    returns None, but changes the cells in the grid to Found.EDGE or Found.LOOP
    """

    # initialize every direction with NOTHING, except the ones that would land us on an already visited cell
    found: dict[tuple[int, int], Found] = {
        direction: Found.NOTHING
        for direction in DIRECTIONS.values()
        if (row + direction[0], col + direction[1]) not in visited
    }

    for direction in found:
        # check if we hit a part of the loop
        if (row + direction[0], col + direction[1]) in loop:
            # check if we can 'squeeze' inbetween pipes
            # determine which of the axes is non-zero and what its value is
            axis, step = [(i, s) for i, s in enumerate(direction) if direction[i] != 0][0]
            pipe = grid[row + direction[0]][col + direction[1]]  # get pipe's directions
            if any(dir[axis] == step for dir in PIPES[pipe]):
                # at least one of the pipe's directions is the same as the current searching direction
                # try to find a way out by squeezing between the pipes
                # this is where I gave up, it's getting too complicated
                pass
            else:
                # none of the pipe's directions are the same as the current searching direction
                found[direction] = Found.LOOP
                continue  # don't look any further in this direction

        # check if we reached a vertical edge
        if not (0 < row + direction[0] < len(grid) - 1):
            found[direction] = Found.EDGE
            break

        # check if we reached a horizontal edge
        if not (0 < col + direction[1] < len(grid[row + direction[0]]) - 1):
            found[direction] = Found.EDGE
            break

        # advance a step in this direction and check if we reached the edge yet
        _find_edge(
            grid,
            loop,
            row + direction[0],
            col + direction[1],
            visited + [(row, col)]  # add current cell to list of visited
        )
        found[direction] = grid[row + direction[0]][col + direction[1]]  # update direction with next cell's value

    if Found.EDGE in found.values():
        grid[row][col] = Found.EDGE
    elif all(f == Found.LOOP == Found.LOOP for d, f in found.items()):
        grid[row][col] = Found.LOOP


def find_enclosed(grid: list[list[str]], loop: list[tuple[int, int]]) -> None:
    """marks all cells in the grid with a member of the Found enum (except outer edges)"""

    # cells in the first and last rows and columns can only be part of the loop or outside the loop
    for r, row in enumerate(grid[1:-1], 1):  # loop through all rows in the grid except the first and last
        for c, char in enumerate(row[1:-1], 1):  # loop through all columns in the current row except the first and last
            if (r, c) in loop:
                continue  # skip any pipe that is part of the loop
            if grid[r][c] == Found.EDGE or grid[r][c] == Found.LOOP:
                continue  # skip cells that have already been visited
            _find_edge(grid, loop, r, c)


def draw_grid(grid: list[list[str|Found]], loop: list[tuple[int, int]]) -> None:
    def num_to_digits(n: int, w: int) -> list[int]:
        return [int(c) for c in f'{n:0{w}}']

    BOLD = '\033[1m'
    FAIL = '\033[91m'  # (red)
    ENDC = '\033[0m'

    height = len(grid)
    row_label_width = len(str(height-1))

    width = len(grid[0])
    col_label_height = len(str(width-1))

    # print column numbers
    for line in range(col_label_height):
        print(' ' * (row_label_width) + ' ', end='')  # reserve space for column numbers
        for col in range(width):
            print(num_to_digits(col,col_label_height)[line], end='')
        print()

    # print lines
    for r, row in enumerate(grid):
        # print the line number
        print(f'{r:{row_label_width}} ', end='')
        for c, char in enumerate(row):
            if (r, c) in loop:
                print(FAIL, end='')
            print(PIPE_TO_BOX[char], end='')
            if (r, c) in loop:
                print(ENDC, end='')

        print(f' {r:{row_label_width}}')

    # print column numbers
    for line in range(col_label_height):
        print(' ' * (row_label_width) + ' ', end='')  # reserve space for column numbers
        for col in range(width):
            print(num_to_digits(col,col_label_height)[line], end='')
        print()

    print()


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid, [])

    start_row, start_col = find_start(grid)
    # print(f'start character "{START}" was found on row {start_row}, column {start_col}')

    loop = find_loop(grid, start_row, start_col)
    # print(loop)

    replace_start(grid, loop)
    # draw_grid([['.'] * 120] * 15, [])
    draw_grid(grid, loop)

    # find_enclosed(grid, loop)
    # draw_grid(grid , loop)

    # print(f'End result: {sum(line.count(Found.LOOP) for line in grid)}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data_1)
    # main(test_data_1a)
    # main(test_data_1b)
    # main(test_data_1c)
    # main(test_data_1d)
    # main(test_data_1e)
    # main(test_data_1f)
    # main(test_data_1g)
    # main(test_data_1h)
    # main(test_data_2a)
    # main(test_data_2b)
    # main(test_data_3)
    # main(test_data_4)
    # main(test_data_4b)
    # main(test_data_5)
    # main(test_data_5a)
    # main(test_data_5b)
    # main(test_data_5c)
    # main(test_data_6)
    # main(test_data_7)

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

# aoc_2023_10_B_1.py - Day 10: Pipe Maze - part 2
# How many tiles are enclosed by the loop?
# https://adventofcode.com/2023/day/10
# found a hint saying I should count the number of pipe edges to the left and to the right of a cell
#   and if both numbers are odd the cell should be considered enclosed
# one problem with that strategy: what exactly is a pipe edge?
# according to some dude on the internet |, F--J and L--7 count as edges, but F--7 and L--J don't
# let's see..


from aoc_2023_10_A_1 import (
    DATA_PATH,
    load_data,
    # test_data_1,
    # test_data_2,
    create_grid,
    find_start,
    find_loop,
    # START,
    PIPES,
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

from aoc_2023_10_B_2 import (
    draw_grid,
    INSIDE,
)

from tools import time_it

from enum import Enum, auto

from pprint import pprint


def _mark_edges(grid: list[list[str]], loop: list[tuple[int]], r: int) -> list[str]:
    """takes one line from the grid and marks all cells that are considered a loop edge"""
    line = []

    prev = ''
    for c, char in enumerate(grid[r]):
        if (r, c) not in loop:
            line.append(' ')
            continue  # skip if this cell isn't part of the loop
        if char == '|':
            line.append('E')  # in/out status changed
        elif char == '-':
            line.append('-')  # in/out status not changed, condition for next edge not changed
        elif char == 'F':
            line.append(' ')
            prev = char  # in/out status changed, condition for next edge changed
        elif char == 'L':
            line.append(' ')
            prev = char  # in/out status changed, condition for next edge changed
        elif char == 'J':
            if prev in list('F'):
                line.append('E')
            else:
                line.append(' ')
            prev = char  # in/out status changed, condition for next edge changed
        elif char == '7':
            if prev in list('L'):
                line.append('E')
            else:
                line.append(' ')
            prev = char  # in/out status changed, condition for next edge changed
        else:
            line.append(' ')

    return line


def find_enclosed(grid: list[list[str]], loop: list[tuple[int, int]]) -> int:
    """returns a list of cells in the grid that are enclosed by the loop"""

    enclosed = 0

    # cells in the first and last rows and columns can only be part of the loop or outside the loop,
    # so we don't bother to check those
    for r, row in enumerate(grid[1:-1], 1):  # loop through all rows in the grid except the first and last
        line = _mark_edges(grid, loop, r)  # mark loop edges for this row
        for c, char in enumerate(line[1:-1], 1):  # loop through all cells in the current line except the first and last
            if (r, c) not in loop:
                left, right = line[:c], line[c+1:]
                if left.count('E') % 2 == 1 and right.count('E') % 2 == 1:
                    enclosed += 1
                    grid[r][c] = INSIDE

    return enclosed


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid, [])

    start_row, start_col = find_start(grid)
    # print(f'start character "{START}" was found on row {start_row}, column {start_col}')

    loop = find_loop(grid, start_row, start_col)
    # print(loop)

    replace_start(grid, loop)
    # draw_grid(grid, loop)

    enclosed = find_enclosed(grid, loop)
    # draw_grid(grid, loop)

    print(f'End result: {enclosed}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data_1)
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

    # using input data:
    #   End result: 601
    #   Finished 'main' in 5.4 seconds

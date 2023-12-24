# aoc_2023_10_B_1.py - Day 10: Pipe Maze - part 2
# find the number of tiles that are enclosed by the loop
# found a hint saying I should count the number of pipe edges to the left and to the right of a cell
#   and if both numbers are odd the cell should be considered enclosed
# one problem with that strategy: what exactly is a pipe edge?
# https://adventofcode.com/2023/day/10


from aoc_2023_10_A import (
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


def _mark_edges(grid, loop, r):
    """takes one line from the grid and marks all cells that are considered a loop edge"""
    line = []
    # line = ['L' if (r, c) in loop else ' ' for c, char in enumerate(grid[r])]  # mark loop pieces for this row

    prev = ''
    for c, char in enumerate(grid[r]):
        if (r, c) not in loop:
            line.append(' ')
            continue  # skip if this cell isn't part of the loop
        if char == '|':
            if prev in '|7J':
                line.append('E')  # in/out status changed
        elif char == '-':
            line.append('-')  # in/out status not changed, condition for next edge not changed
        elif char == 'F':
            if prev in '|7J':
                line.append('E')
            prev = char  # in/out status changed, condition for next edge changed
        elif char == 'J':
            if prev in '|L':
                line.append('E')
            elif prev in 'F':
                line.append(' ')
            prev = char  # in/out status changed, condition for next edge changed
        elif char == 'L':
            if prev in '|J7':
                line.append('E')
            prev = char  # in/out status changed, condition for next edge changed
        elif char == '7':
            if prev in '|LF':
                line.append('E')
            elif prev in 'L':
                line.append(' ')
            prev = char  # in/out status changed, condition for next edge changed
        else:
            line.append(' ')

    return line


def find_enclosed(grid: list[list[str]], loop: list[tuple[int]]) -> int:
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


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_1a
    # data_lines = test_data_1b
    # data_lines = test_data_1c
    # data_lines = test_data_1d
    # data_lines = test_data_1e
    # data_lines = test_data_1f
    # data_lines = test_data_1g
    # data_lines = test_data_1h
    # data_lines = test_data_2a
    # data_lines = test_data_2b
    # data_lines = test_data_3
    # data_lines = test_data_4
    # data_lines = test_data_4b
    # data_lines = test_data_5
    # data_lines = test_data_5a
    # data_lines = test_data_5b
    # data_lines = test_data_5c
    data_lines = test_data_6
    # data_lines = test_data_7
    # print(data_lines)

    grid = create_grid(data_lines)
    # draw_grid(grid)

    start_row, start_col = find_start(grid)
    # print(f'start character "{START}" was found on row {start_row}, column {start_col}')


    loop = find_loop(grid, start_row, start_col)
    # print(loop)

    replace_start(grid, loop)
    draw_grid(grid)

    enclosed = find_enclosed(grid, loop)
    draw_grid(grid)

    print(f'End result: {enclosed}')

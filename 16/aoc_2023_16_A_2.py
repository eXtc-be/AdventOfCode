# aoc_2023_16_A_1.py - Day 16: The Floor Will Be Lava - part 1
# The light isn't energizing enough tiles to produce lava; to debug the contraption,
# you need to start by analyzing the current situation. With the beam starting in the top-left heading right,
# how many tiles end up being energized?
# this version will try a different loop detecting strategy: for each cell on the grid, keep track of the
#   directions from which it has been entered and stop a particular path if all 4 directions are used
# https://adventofcode.com/2023/day/16


from aoc_2023_16_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_grid,
    draw_grid,
)

from tools import time_it

import sys

from pprint import pprint


DIRECTIONS = {
    1: (1, 0),  # DOWN
    2: (-1, 0),  # UP
    3: (0, 1),  # RIGHT
    4: (0, -1),  # LEFT
}

MAX_VISIT = 10


def draw_energized(energized: list[list[list[str | bool | int]]]) -> None:
    """draws the energized grid"""
    for row in energized:
        print(''.join([cell[0] for cell in row]))
    print('-' * 100)


def _travel_grid(
        grid: list[list[str]],
        energized: list[list[list[str | bool | int]]],
        row: int,
        col: int,
        dir: int
) -> None:
    delta_r, delta_c = DIRECTIONS[dir]

    while True:
        energized[row][col][0] = '#'
        energized[row][col][dir] = True  # dir: 1 to 4
        energized[row][col][5] += 1  # visited counter

        # calculate next cell
        row += delta_r
        col += delta_c

        # verify bounds
        if row < 0 or row > len(grid) - 1 or col < 0 or col > len(grid[row]) - 1:
            break  # when we hit the edge of the grid we stop

        if all(energized[row][col][1:-1]):  # already visited from all directions
            break

        if energized[row][col][5] > MAX_VISIT:  # visited too much
            break

        next_cell = grid[row][col]

        if next_cell == '.':  # continue in same direction
            continue
        elif next_cell == '/':  # deflect right to up, left to down, up to right, down to left
            rr = 0 if delta_r else -delta_c
            cc = 0 if delta_c else -delta_r
            delta_r, delta_c = rr, cc
        elif next_cell == '\\':  # deflect right to down, left to up, up to left, down to right
            rr = 0 if delta_r else delta_c
            cc = 0 if delta_c else delta_r
            delta_r, delta_c = rr, cc
        elif next_cell == '|':  # split horizontal beam to 2 verticals, pass vertical beam
            if delta_c:  # split horizontal beam
                _travel_grid(grid, energized, row, col, 1)  # split to down
                _travel_grid(grid, energized, row, col, 2)  # split to up
                break  # don't continue
            else:  # pass through
                continue
        elif next_cell == '-':  # split vertical beam to 2 horizontals, pass horizontal beam
            if delta_r:  # split vertical beam
                _travel_grid(grid, energized, row, col, 3)  # split to the right
                _travel_grid(grid, energized, row, col, 4)  # split to the left
                break  # don't continue
            else:  # pass through
                continue


def find_energized(grid: list[list[str]]) -> list[list[list[str | bool | int]]]:
    """follows the beam around the grid and marks the tiles where
    the beam passes as energized"""
    # create an empty grid the same size as the original
    energized = [[['.', False, False, False, False, 0] for _ in range(len(row))] for row in grid]

    row, col, dir = 0, 0, 3  # upper left corner, direction 3 (right)

    _travel_grid(grid, energized, row, col, dir)

    return energized


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid)

    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(100000)
    energized = find_energized(grid)
    sys.setrecursionlimit(old_limit)
    draw_energized(energized)

    print(f'End result: {sum(sum(cell[0] == "#" for cell in row) for row in energized)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 46
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 8037 (MAX_VISIT=10) - incorrect
    #   Finished 'main' in 27 milliseconds

    # test find_energized
    # grid = create_grid(['.....', '.....', '.....', '.....', '.....'])  # no mirrors, straight through
    # grid = create_grid(['...\\.', '.....', '.....', '.....', '.....'])  # 1 mirror
    # grid = create_grid(['..\\..', '.....', '.....', '..\\..', '.....'])  # 2 identical mirrors
    # grid = create_grid(['....\\', '.....', '.....', '.....', '..../'])  # 2 opposite mirrors
    # grid = create_grid(['..\\..', '.....', '.....', '..-..', '.....'])  # horizontal splitter
    # grid = create_grid(['.\\...', '.....', '.....', '.\\..|', '.....'])  # vertical splitter
    # grid = create_grid(['....\\', '....-', '.....', '.....', '.....'])  # horizontal splitter at edge
    # grid = create_grid(['.-\\..', '.....', '.\\/..', '.....', '.....'])  # loop
    # draw_grid(grid)
    # energized = find_energized(grid)
    # draw_energized(energized)

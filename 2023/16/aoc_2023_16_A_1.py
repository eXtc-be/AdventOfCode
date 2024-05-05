# aoc_2023_16_A_1.py - Day 16: The Floor Will Be Lava - part 1
# The light isn't energizing enough tiles to produce lava; to debug the contraption,
# you need to start by analyzing the current situation. With the beam starting in the top-left heading right,
# how many tiles end up being energized?
# https://adventofcode.com/2023/day/16
# this version ends in a very reasonable time (less than a second), but fails to give the correct answer


from tools import time_it

import sys

from pprint import pprint


DATA_PATH = './input_2023_16'

MAX_VISIT = 10


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_grid(data_lines: list[str]) -> list[list[str]]:
    return [[char for char in line] for line in data_lines]


def draw_grid(grid: list[list[str]]) -> None:
    """draws the grid"""
    for row in grid:
        print(''.join(row))
    print('-' * 100)


def draw_energized(grid: list[list[int]]) -> None:
    """draws the energized grid"""
    for row in grid:
        print(''.join(['#' if cell else '.' for cell in row]))
    print('-' * 100)


def _travel_grid(
        grid: list[list[str]],
        energized: list[list[int]],
        row: int,
        col: int,
        dir: tuple[int, int]
) -> None:
    delta_r, delta_c = dir

    while True:
        energized[row][col] += 1

        # calculate next cell
        row += delta_r
        col += delta_c

        # verify bounds
        if row < 0 or row > len(grid) - 1 or col < 0 or col > len(grid[row]) - 1:
            break  # when we hit the edge of the grid we stop

        if energized[row][col] >= MAX_VISIT:  # already visited enough
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
                _travel_grid(grid, energized, row, col, (1, 0))  # split to down
                _travel_grid(grid, energized, row, col, (-1, 0))  # split to up
                break  # don't continue
            else:  # pass through
                continue
        elif next_cell == '-':  # split vertical beam to 2 horizontals, pass horizontal beam
            if delta_r:  # split vertical beam
                _travel_grid(grid, energized, row, col, (0, 1))  # split to the right
                _travel_grid(grid, energized, row, col, (0, -1))  # split to the left
                break  # don't continue
            else:  # pass through
                continue


def find_energized(grid: list[list[str]]) -> list[list[int]]:
    """follows the beam around the grid and marks the tiles where
    the beam passes as energized"""
    # create an empty grid the same size as the original
    energized = [[0] * len(line) for line in grid]

    row, col, dir = 0, 0, (0, 1)

    _travel_grid(grid, energized, row, col, dir)

    return energized


test_data = r'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid)

    # old_limit = sys.getrecursionlimit()
    # sys.setrecursionlimit(100000)
    energized = find_energized(grid)
    # sys.setrecursionlimit(old_limit)
    draw_energized(energized)

    print(f'End result: {sum(sum(cell>0 for cell in row) for row in energized)}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 46
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 7956 (MAX_VISIT=4) - too low
    #   Finished 'main' in 6 milliseconds
    #   End result: 8091 (MAX_VISIT=10) - too low
    #   Finished 'main' in 12 milliseconds
    #   End result: 8091 (MAX_VISIT=100) - not submitted
    #   Finished 'main' in 108 milliseconds
    #   End result: 8091 (MAX_VISIT=250) - not submitted
    #   Finished 'main' in 292 milliseconds

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

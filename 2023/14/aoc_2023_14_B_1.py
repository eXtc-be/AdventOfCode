# aoc_2023_14_B_1.py - Day 14: Parabolic Reflector Dish - part 2
# Tilt the platform a large number of times.
# Afterward, what is the total load on the north support beams?
# https://adventofcode.com/2023/day/14
# this unoptimized version runs for over 2 minutes with test_data (10x10) and only 1_000_000 cycles,
#   so no way we're going to even try with the input data (100x100) and 1_000_000_000 cycles before optimizing


from aoc_2023_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_grid,
    tilt_grid,
    calc_load,
)

from tools import time_it

# other imports

from pprint import pprint


CYCLES = 1_000
# CYCLES = 1_000_000
# CYCLES = 1_000_000_000


def _rotate_grid(grid: list[list[str]], orientation: str) -> list[list[str]]:
    rotated_grid = [[cell for cell in line] for line in grid]  # copy grid

    if orientation.lower() in 'sw':
        rotated_grid = [[e for e in row[::-1]] for row in rotated_grid[::-1]]  # turn grid 180 degrees
    if orientation.lower() in 'ew':
        rotated_grid = list(zip(*rotated_grid[::-1]))  # turn grid 90 degrees CW

    return [list(row) for row in rotated_grid]  # convert tuples back to lists


def cycle_grid(grid: list[list[str]]) -> list[list[str]]:
    cycled_grid = [[cell for cell in line] for line in grid]  # copy grid

    # to tilt the grid to the north, just call tilt_grid with the grid
    cycled_grid = tilt_grid(cycled_grid)

    # to tilt the grid to the west, rotate it to the east first,
    # then call tilt_grid with the rotated grid and finally rotate it back
    cycled_grid = _rotate_grid(tilt_grid(_rotate_grid(cycled_grid, 'E')), 'W')

    # to tilt the grid to the south, rotate it to the south first,
    # then call tilt_grid with the rotated grid and finally rotate it back
    cycled_grid = _rotate_grid(tilt_grid(_rotate_grid(cycled_grid, 'S')), 'S')

    # to tilt the grid to the east, rotate it to the west first,
    # then call tilt_grid with the rotated grid and finally rotate it back
    cycled_grid = _rotate_grid(tilt_grid(_rotate_grid(cycled_grid, 'W')), 'E')

    return cycled_grid


def draw_grid(grid: list[list[str]]) -> None:
    """draws the grid"""
    for row in grid:
        print(''.join(row))
    print('-' * 100)


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid)

    cycled_grid = grid
    for _ in range(CYCLES):
        cycled_grid = cycle_grid(cycled_grid)

    load = calc_load(cycled_grid)
    print(load)

    print(f'End result: {sum(load)} after {CYCLES:,} cycles')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 64 after 1,000 cycles
    #   Finished 'main' in 155 milliseconds
    #   End result: 65 after 1,000,000 cycles
    #   Finished 'main' in 2 minutes and 29 seconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

    # test _rotate_grid
    # n_grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    # draw_grid(n_grid)
    #
    # e_grid = _rotate_grid(n_grid,'E')
    # draw_grid(e_grid)
    #
    # s_grid = _rotate_grid(n_grid,'S')
    # draw_grid(s_grid)
    #
    # w_grid = _rotate_grid(n_grid,'W')
    # draw_grid(w_grid)

    # test cycle_grid
    # cycled_grid = cycle_grid(grid)
    # draw_grid(cycled_grid)
    # cycled_grid = cycle_grid(cycled_grid)
    # draw_grid(cycled_grid)
    # cycled_grid = cycle_grid(cycled_grid)
    # draw_grid(cycled_grid)


# aoc_2023_16_B_1.py - Day 16: The Floor Will Be Lava - part 2
# Find the initial beam configuration that energizes the largest number of tiles;
# how many tiles are energized in that configuration?
# https://adventofcode.com/2023/day/16


from aoc_2023_16_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_grid,
    draw_grid,
)

from aoc_2023_16_A_3 import (
    draw_energized,
    _travel_grid,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def find_energized(grid: list[list[str]], row: int, col: int, dir: int) -> list[list[list[str | bool | int]]]:
    """creates the energized grid based on the dimensions of the original grid,
    calls _travel_grid() and returns the energized grid for the given start row, col and dir"""

    # create an empty grid the same size as the original
    energized = [[['.', False, False, False, False] for _ in range(len(row))] for row in grid]

    _travel_grid(grid, energized, row, col, dir)

    return energized


def _calc_energized_sum(energized: list[list[list[str | bool | int]]]) -> int:
    return sum(sum(cell[0] == "#" for cell in row) for row in energized)


def find_most_energized(grid: list[list[str]]) -> dict[tuple[int, int, int], int]:
    results = {}

    # loop through all rows and calculate the total energy for both directions left and right
    for r in range(len(grid)):
        results[(r, 0, 3)] = _calc_energized_sum(find_energized(grid, r, 0, 3))
        results[(r, len(grid[r])-1, 4)] = _calc_energized_sum(find_energized(grid, r, len(grid[r])-1, 4))

    # loop through all columns and calculate the total energy for both directions up and down
    for c in range(len(grid[0])):  # assume all rows are the same length
        results[(0, c, 1)] = _calc_energized_sum(find_energized(grid, 0, c, 1))
        results[(len(grid)-1, c, 2)] = _calc_energized_sum(find_energized(grid, len(grid)-1, c, 2))

    return results


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid)

    results = find_most_energized(grid)
    # pprint(results)

    print(f'End result: {max(results.values())}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 51
    #   Finished 'main' in 2 milliseconds
    # using input data:
    #   End result: 8335
    #   Finished 'main' in 4.8 seconds

    # test find_energized with row, col, dir
    # energized = find_energized(create_grid(data_lines), 0, 3, 1)
    # draw_energized(energized)
    # print(_calc_energized_sum(energized))

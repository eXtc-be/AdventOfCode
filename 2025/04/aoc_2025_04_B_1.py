# aoc_2025_04_B_1.py - Day 4: Printing Department - part 2
# How many rolls of paper in total can be removed by the Elves and their forklifts?
# https://adventofcode.com/2025/day/4


from aoc_2025_04_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    count_adjacent,
    Coord,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions
def remove_accessible(grid: list[list[str]]) -> int:
    removed = 0

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if count_adjacent(grid, Coord(col, row)) < 4 and grid[row][col] == '@':
                grid[row][col] = 'x'
                removed += 1

    return removed


@time_it
def main(data_lines: list[str]) -> None:
    grid = [[char for char in line] for line in data_lines]

    total = 0

    while True:
        removed = remove_accessible(grid)
        if removed == 0:
            break
        else:
            total += removed

    print(f'End result: {total}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 43
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 7922
    #   Finished 'main' in 2.2 seconds

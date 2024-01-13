# aoc_2015_18_B_1.py - Day 18: Like a GIF For Your Yard - part 2
# In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?
# https://adventofcode.com/2015/day/18


from aoc_2015_18_A_1 import (
    DATA_PATH,
    load_data,
    test_data, _count_neighbours, ON, OFF, get_grid, STEPS
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def do_step(grid: list[list[str]]) -> list[list[str]]:
    result = []
    for r, row in enumerate(grid):
        result_row = []
        for c, cell in enumerate(row):
            if (
                    r == 0 and c == 0 or
                    r == 0 and c == len(grid[r]) - 1 or
                    r == len(grid) - 1 and c == 0 or
                    r == len(grid) - 1 and c == len(grid[r]) - 1
            ):
                result_row.append(ON)
                continue
            neighbours = _count_neighbours(r, c, grid)
            if cell == ON:
                if neighbours in (2, 3):
                    result_row.append(ON)
                else:
                    result_row.append(OFF)
            else:
                if neighbours == 3:
                    result_row.append(ON)
                else:
                    result_row.append(OFF)
        result.append(result_row)

    return result


@time_it
def main(data_lines: list[str]) -> None:
    grid = get_grid(data_lines)
    # print('\n'.join(''.join(char for char in row) for row in grid))
    # print('=' * 100)

    grid[0][0] = ON
    grid[0][-1] = ON
    grid[-1][0] = ON
    grid[-1][-1] = ON
    # print('\n'.join(''.join(char for char in row) for row in grid))
    # print('=' * 100)

    new_grid = grid  # initial value
    for _ in range(STEPS):
        new_grid = do_step(new_grid)
        # print('\n'.join(''.join(char for char in row) for row in new_grid))
        # print('-' * 100)

    print(f'End result: {sum(row.count(ON) for row in new_grid)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 17
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 781
    #   Finished 'main' in 2.3 seconds

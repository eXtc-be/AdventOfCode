# aoc_2015_06_B_1.py - Day 6: Probably a Fire Hazard - part 2
# After following the instructions, how many lights are lit?
# https://adventofcode.com/2015/day/6


from aoc_2015_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# GRID_SIZE = 10
GRID_SIZE = 1000


def follow_instructions(instructions: list[str], grid: list[list[int]]) -> None:
    for instruction in instructions:
        parts = instruction.split()
        if parts[0] == 'turn':
            x1, y1 = map(int, parts[2].split(','))
            x2, y2 = map(int, parts[4].split(','))

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if parts[1] == 'on':
                        grid[y][x] += 1
                    else:
                        grid[y][x] -= 1
                        if grid[y][x] < 0:
                            grid[y][x] = 0
        elif parts[0] == 'toggle':
            x1, y1 = map(int, parts[1].split(','))
            x2, y2 = map(int, parts[3].split(','))

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    grid[y][x] += 2
        else:
            print(f'Invalid instruction: {instruction}')


@time_it
def main(data_lines: list[str]) -> None:
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    # print('\n'.join(''.join(str(char) for char in row) for row in grid))

    # print('-' * 100)

    follow_instructions(data_lines, grid)
    # print('\n'.join(''.join(str(char) for char in row) for row in grid))

    print(f'End result: {sum(sum(cell for cell in row) for row in grid)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 13396307 - too low
    #               14110788
    #   Finished 'main' in 2.1 seconds

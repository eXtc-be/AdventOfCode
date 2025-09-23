# aoc_2024_04_B_1.py - Day 4: Ceres Search - part 2
# Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
# https://adventofcode.com/2024/day/4


from aoc_2024_04_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants

FIND = 'MAS'

DIRECTIONS = (
    (1, 1),
    (-1, 1),
)


# other functions

def count_words(data_lines: list[str]) -> int:
    total = 0

    for y, line in enumerate(data_lines):
        for x, char in enumerate(line):
            if data_lines[y][x] == FIND[1]:
                total += check_X(data_lines, x, y)

    return total


def check_X(data_lines: list[str], x: int, y: int) -> int:
    return 1 if check_direction(data_lines, x, y, 1, 1) and \
                check_direction(data_lines, x, y, -1, 1) else 0


def check_direction(data_lines: list[str], x: int, y: int, dx: int, dy: int) -> bool:
    if y + dy < 0 or y + dy > len(data_lines) - 1:
        return False
    if y - dy < 0 or y - dy > len(data_lines) - 1:
        return False
    if x - dx < 0 or x - dx > len(data_lines[0]) - 1:
        return False
    if x + dx < 0 or x + dx > len(data_lines[0]) - 1:
        return False

    return True if data_lines[y + dy][x + dx] == FIND[0] and  data_lines[y - dy][x - dx] == FIND[-1] or \
                   data_lines[y + dy][x + dx] == FIND[-1] and data_lines[y - dy][x - dx] == FIND[0] else False


@time_it
def main(data_lines: list[str]) -> None:
    result = count_words(data_lines)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 9
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1877
    #   Finished 'main' in 6 milliseconds

# aoc_2015_01_B_1.py - Day 1: Not Quite Lisp - part 2
# What is the position of the character that causes Santa to first enter the basement?
# https://adventofcode.com/2015/day/1


from aoc_2015_01_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    UP,
    DN,
)

from tools import time_it

# other imports


# other constants


def find_basement(instructions: str) -> int:
    floor = 0
    for i, instruction in enumerate(instructions, 1):
        floor += 1 if instruction == UP else -1
        if floor < 0:
            return i

    return -1 # if not found


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, find_basement(line))

    print(f'End result: {find_basement(data_lines[0])}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 1795
    #   Finished 'main' in less than a millisecond

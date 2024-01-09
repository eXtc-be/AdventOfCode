# aoc_2015_03_B_1.py - Day 3: Perfectly Spherical Houses in a Vacuum - part 2
# How many houses receive at least one present from Santa and Robo-Santa?
# https://adventofcode.com/2015/day/3


from aoc_2015_03_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    find_houses,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def find_split_houses(instructions: str) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    return find_houses(instructions[::2]), find_houses(instructions[1::2])


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, find_split_houses(line))

    # santa, robo = find_split_houses('^v')
    santa, robo = find_split_houses(data_lines[0])

    print(f'End result: {len(santa | robo)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 2360 - too high
    #               2359 - too high
    #               2341 - correct
    #   Finished 'main' in 9 milliseconds

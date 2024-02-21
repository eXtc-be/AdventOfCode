# aoc_2017_02_B_1.py - Day 2: Corruption Checksum - part 2
# What is the checksum for the spreadsheet in your puzzle input?
# https://adventofcode.com/2017/day/2


from aoc_2017_02_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_data,
)

from tools import time_it

from itertools import permutations

from pprint import pprint


# other constants


def checksum(data: list[list[int]]) -> int:
    return sum(
        first // second
        for row in data for first, second in permutations(row, 2)
        if first % second == 0
    )


test_data = '''
5 9 2 8
9 4 7 3
3 8 6 5
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    data = get_data(data_lines)
    # print(data)

    print(f'End result: {checksum(data)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 9
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 250
    #   Finished 'main' in 1 millisecond

# aoc_2016_10_B_1.py - Day 10: Balance Bots - part 2
# What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?
# https://adventofcode.com/2016/day/10


from aoc_2016_10_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    Factory,
)

from tools import time_it

from operator import mul
from functools import reduce

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str], goal: tuple[int, int]) -> None:
    factory = Factory()
    # pprint(factory)

    factory.get_instructions(data_lines)
    # pprint(factory)

    factory.execute_instructions()
    # pprint(factory)

    print(f'End result: {reduce(mul, [output.value for output in factory.outputs if output.id in (0, 1, 2)], 1)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    # main(data_lines, (2, 5))  # test
    main(data_lines, (17, 61))  # for real
    # using test_data:
    #   End result: 30
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4042
    #   Finished 'main' in 4 milliseconds

# aoc_2015_20_B_1.py - Day 20: Infinite Elves and Infinite Houses - part 2
# What is the lowest house number of the house to get at least as many presents as the number in your puzzle input,
# given that each elf now stops after delivering to 50 houses, but delivers 11 times its number to each house?
# https://adventofcode.com/2015/day/20


from aoc_2015_20_A_2 import (
    DATA_PATH,
    load_data,
    _find_divisors,
)

from tools import time_it

from itertools import combinations
from functools import reduce
from operator import mul

from pprint import pprint


FACTOR = 11
LIMIT = 50


def _calc_house(house: int) -> int:
    return sum(num * FACTOR for num in _find_divisors(house) if house // num <= LIMIT)


def find_target_house(target: int) -> int:
    house = 1

    while True:
        value = _calc_house(house)
        if value >= target:
            break
        house += 1

    return house


test_data = '''
10_000_000
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    target = int(data_lines[0])

    result = find_target_house(target)

    print(f'End result: {result}: {_calc_house(result-1)} - {_calc_house(result)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data 1_000:
    #   End result: 36: 528 - 1001
    #   Finished 'main' in less than a millisecond
    # using test_data 10_000:
    #   End result: 336: 336: 4422 - 10736
    #   Finished 'main' in 2 milliseconds
    # using test_data 100_000:
    #   End result: 2880: 31669 - 104742
    #   Finished 'main' in 21 milliseconds
    # using test_data 1_000_000:
    #   End result: 25200: 277189 - 1021482
    #   Finished 'main' in 266 milliseconds
    # using test_data 10_000_000:
    #   End result: 249480: 2744269 - 10340715
    #   Finished 'main' in 4.6 seconds
    # using input data:
    #   End result: 705600: 8029230 - 29002446
    #   Finished 'main' in 15 seconds

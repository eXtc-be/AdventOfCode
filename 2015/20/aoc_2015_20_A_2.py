# aoc_2015_20_A_2.py - Day 20: Infinite Elves and Infinite Houses - part 1
# What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?
# https://adventofcode.com/2015/day/20

# with a target of 1 million, the unoptimized version ran for 22 seconds,
# 80 times longer than for a target 10 times smaller
# knowing the actual target is 29 million, I estimate a run time of about 18 hours
# time for the first optimization: finding all divisors of a number instead of looping through
#   all numbers up to that number and testing if the number is divisible


from aoc_2015_20_A_1 import (
    DATA_PATH,
    load_data,
    FACTOR,
)

from tools import time_it

from itertools import combinations
from functools import reduce
from operator import mul

from pprint import pprint


# other constants


def _find_prime_factors(number: int) -> list[int]:
    i = 2
    factors = []
    while i * i <= number:
        if number % i:
            i += 1
        else:
            number //= i
            factors.append(i)
    if number > 1:
        factors.append(number)
    return factors


def _find_divisors(number: int) -> set[int]:
    divisors = {1}

    prime_factors = _find_prime_factors(number)

    for r in range(1, len(prime_factors)+1):
        for product in set(combinations(prime_factors, r)):
            divisors.add(reduce(mul, product, 1))

    return divisors


def _calc_house(house: int) -> int:
    return sum(num * FACTOR for num in _find_divisors(house))


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
    #   End result: 48: 480 - 1240
    #   Finished 'main' in less than a millisecond
    # using test_data 10_000:
    #   End result: 360: 3600 - 11700
    #   Finished 'main' in 2 milliseconds
    # using test_data 100_000:
    #   End result: 3120: 31200 - 104160
    #   Finished 'main' in 23 milliseconds
    # using test_data 1_000_000:
    #   End result: 27720: 282960 - 1123200
    #   Finished 'main' in 288 milliseconds
    # using test_data 10_000_000:
    #   End result: 249480: 2505840 - 10454400
    #   Finished 'main' in 4.2 seconds
    # using input data:
    #   End result: 665280: 6652800 - 29260800
    #   Finished 'main' in 14 seconds

    # # test _find_divisors
    # print(_find_divisors(12))
    # print(_find_divisors(20))
    # print(_find_divisors(100))
    # print(_find_divisors(666))

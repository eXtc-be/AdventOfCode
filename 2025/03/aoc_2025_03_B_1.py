# aoc_2025_03_B_1.py - Day 3: Lobby - part 2
# What is the new total output joltage?
# https://adventofcode.com/2025/day/3
from functools import reduce

from aoc_2025_03_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants
DIGITS = 12


# other functions
def get_max_jolt(bank: str) -> int:
    numbers = []
    start = 0

    for digit in range(DIGITS):
        number = max(int(digit) for digit in bank[start:len(bank)-(DIGITS-1-digit)])
        start = bank.index(str(number), start) + 1
        numbers.append(number)

    return reduce(lambda total, num: 10 * total + num, numbers)


@time_it
def main(data_lines: list[str]) -> None:
    result = sum(get_max_jolt(line) for line in data_lines)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 3121910778619
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 172740584266849
    #   Finished 'main' in 12 milliseconds

# aoc_2015_12_B_1.py - Day 12: JSAbacusFramework.io - part 2
# What is the sum of all numbers in the document?
# https://adventofcode.com/2015/day/12


from aoc_2015_12_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

import json

from pprint import pprint


# other constants


def find_numbers(object: dict) -> list[int]:
    numbers = []

    if isinstance(object, dict):
        if 'red' in object.values():
            return numbers
        for k, v in object.items():
            numbers += find_numbers(v)
    elif isinstance(object, list):
        for e in object:
            numbers += find_numbers(e)
    elif isinstance(object, int):
        numbers += [object]

    return numbers


@time_it
def main(data_lines: list[str]) -> None:
    for line in data_lines:
        numbers = find_numbers(json.loads(line))
        # print(numbers, sum(numbers))

    print(f'End result: {sum(numbers)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 65402
    #   Finished 'main' in 1 millisecond

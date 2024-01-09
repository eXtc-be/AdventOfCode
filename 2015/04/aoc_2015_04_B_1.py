# aoc_2015_04_B_1.py - Day 4: The Ideal Stocking Stuffer - part 2
# Find the lowest positive number that produces a hash starting with 6 zeroes
# https://adventofcode.com/2015/day/4


from aoc_2015_04_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    find_lowest_hash,
)

from tools import time_it

# other imports

from pprint import pprint


THRESHOLD = 6


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    result = find_lowest_hash(data_lines[0], THRESHOLD)

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 9962624
    #   Finished 'main' in 33 seconds

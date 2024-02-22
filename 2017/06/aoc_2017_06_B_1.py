# aoc_2017_06_B_1.py - Day 6: Memory Reallocation - part 2
# How many cycles are in the infinite loop?
# https://adventofcode.com/2017/day/6


from aoc_2017_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,get_banks,
    redistribute_banks
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


@time_it
def main(data_lines: list[str]) -> None:
    banks = get_banks(data_lines[0])
    # print(banks)

    states = redistribute_banks(banks)
    # print(states)

    print(f'End result: {len(states) - states.index(states[-1]) - 1}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 8038
    #   Finished 'main' in 1.62 seconds

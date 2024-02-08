# aoc_2015_24_B_1.py - Day 24: It Hangs in the Balance - part 2
# What is the quantum entanglement of the first group of packages in the ideal configuration?
# https://adventofcode.com/2015/day/24


from aoc_2015_24_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    main,
)

from tools import time_it

# other imports

from pprint import pprint


NUM_GROUPS = 4


# other functions


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, NUM_GROUPS)
    # using test_data:
    #   End result: 44
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 80393059
    #   Finished 'main' in 5 milliseconds

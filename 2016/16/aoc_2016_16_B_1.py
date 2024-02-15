# aoc_2016_16_B_1.py - Day 16: Dragon Checksum - part 2
# The first disk you have to fill has length 272. Using the initial state in your puzzle input, what is the correct checksum?
# https://adventofcode.com/2016/day/16


from aoc_2016_16_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    do_dragon,
    checksum
)

from tools import time_it

# other imports

from pprint import pprint


LIMIT_REAL = 35651584


# other functions


@time_it
def main(initial: str, limit: int) -> None:
    # print(initial)
    d = do_dragon(initial, limit)
    # print(d)
    c = checksum(d[:limit])
    # print(c)

    print(f'End result: {c}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    limit = LIMIT_REAL
    # limit = LIMIT_TEST
    # print(data_lines)

    main(data_lines[0], limit)
    # using input data:
    #   End result: 01010100101011100
    #   Finished 'main' in 25 seconds

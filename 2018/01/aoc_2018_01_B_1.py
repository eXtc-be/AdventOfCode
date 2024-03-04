# aoc_2018_01_B_1.py - Day 1: Chronal Calibration - part 2
# What is the first frequency your device reaches twice?
# https://adventofcode.com/2018/day/1


from aoc_2018_01_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

from itertools import cycle

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    freq = 0
    freqs = set()

    for line in cycle(data_lines):
        freq += int(line)
        if freq in freqs:
            break
        freqs.add(freq)

    print(f'End result: {freq}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 71892
    #   Finished 'main' in 31 milliseconds

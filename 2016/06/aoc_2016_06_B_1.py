# aoc_2016_06_B_1.py - Day 6: Signals and Noise - part 2
# Given the recording in your puzzle input, what is the error-corrected version of the message being sent?
# https://adventofcode.com/2016/day/6


from aoc_2016_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

from collections import Counter

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    message = ''

    for i in range(len(data_lines[0])):
        counter = Counter()
        for line in data_lines:
            counter[line[i]] += 1
        message += counter.most_common()[-1][0]

    print(f'End result: {message}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: advent
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: xrwcsnps
    #   Finished 'main' in 1 millisecond

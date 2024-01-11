# aoc_2015_10_B_1.py - Day 10: Elves Look, Elves Say - part 2
# Starting with the digits in your puzzle input, apply this process 50 times.  What is the length of the result?
# https://adventofcode.com/2015/day/10


from aoc_2015_10_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    REPEATS,
    look_and_say,
)

from tools import time_it

# other imports

from pprint import pprint


NEW_REPEATS = 50


@time_it
def main(data_lines: list[str]) -> None:
    result = data_lines[0]
    # result = 492982
    # print(result)

    for _ in range(NEW_REPEATS - REPEATS + 1):
        result = look_and_say(result)
        # print(result)

    print(f'End result: {len(result):,}')

    # for _ in range(NEW_REPEATS - REPEATS):
    #     result = calculate_conway(result)
    #     # print(result)
    #
    # print(f'End result: {round(result):,}')


if __name__ == "__main__":
    data_lines = load_data('input_2015_10_2')
    # data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 1,166,642 - too low - in 2.9 seconds
    #               6,985,524 - too low - in less than a millisecond
    #               9,106,170 - too high - in less than a millisecond
    #               6,985,522 - incorrect - in less than a millisecond
    #               9,106,167 - incorrect - in less than a millisecond
    #               6,989,950 in 8.4 seconds

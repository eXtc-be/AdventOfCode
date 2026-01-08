# aoc_2023_06_B_2.py - Day 6: Wait For It - part 2
# How many ways can you beat the record in this one much longer race?
# https://adventofcode.com/2023/day/6
# same formula as aoc_2023_06_A_2, only difference is the time and distance values are now concatenated
# and only 1 calculation is necessary


from aoc_2023_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from aoc_2023_06_A_2 import calc_limits_for_race

from aoc_2023_06_B_1 import create_race

from tools import time_it

from math import floor, ceil

from pprint import pprint


# other constants


@time_it
def main(data_lines: list[str]) -> None:
    race = create_race(data_lines)
    # print(race)

    left_limit, right_limit = calc_limits_for_race(*race)
    # print(left_limit, right_limit)

    # add/subtract a very small number (1e-8) so if any of the limits is exactly equal to the record
    #   the floor and ceiling function will round to the next lower/higher integer
    #   (only distances greater than the record count, not greater than or equal)
    # print(ceil(left_limit + 1e-8), floor(right_limit - 1e-8))

    print(f'End result: {floor(right_limit - 1e-8) - ceil(left_limit + 1e-8) + 1}')  # 30125202


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 71503
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 30125202
    #   Finished 'main' in less than a millisecond

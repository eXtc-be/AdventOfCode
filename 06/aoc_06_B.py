# aoc_06_B.py - Day 6: Wait For It - part 2
# use button press to beat records
# same formula as aoc_06_A_2, only difference is the time and distance values are now concatenated
# and only 1 calculation is necessary
# https://adventofcode.com/2023/day/6


from aoc_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)
from aoc_06_A_2 import calc_limits_for_race
from math import floor, ceil


def create_race(data_lines):
    for line in data_lines:
        if line.strip().lower().startswith('time:'):
            time = int(''.join(line.strip().split()[1:]))
        if line.strip().lower().startswith('distance:'):
            distance = int(''.join(line.strip().split()[1:]))
    return time, distance


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    race = create_race(data_lines)
    print(race)

    left_limit, right_limit = calc_limits_for_race(*race)
    print(left_limit, right_limit)
    # add/subtract a very small number (1e-8) so if any of the limits is exactly equal to the record
    #   the floor and ceiling function will round to the next lower/higher integer
    #   (only distances greater than the record count, not greater than or equal)
    print(ceil(left_limit + 1e-8), floor(right_limit - 1e-8))
    print(floor(right_limit - 1e-8) - ceil(left_limit + 1e-8) + 1)

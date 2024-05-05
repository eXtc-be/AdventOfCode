# aoc_2023_06_A_1.py - Day 6: Wait For It - part 1
# Determine the number of ways you could beat the record in each race.
# What do you get if you multiply these numbers together?
# https://adventofcode.com/2023/day/6
# non-naive version: calculate lower and upper limits for button presses
#                    where the distance traveled is larger than the record
# distance = time_left * speed, where
#   time_left = total_time - time_pressed, and
#   speed = 1mm/s * time_pressed, so
# distance = (total_time - time_pressed) * time_pressed = - time_pressed^2 + total_time * time_pressed
# so for distance = y, time_pressed = x, total_time = t
#   y = -x^2 + tx + 0, so with y = rec that becomes rec = -x^2 + tx + 0 or 0 = -x^2 + tx - rec
#       if we say a = -1, b = t, c = -rec that becomes ax^2 + bx + c = 0
#       and from calculus we know x = 0 for (-b +/- sqrt(D)) / 2a where D = b^2 - 4ac
#       so left limit x1 = (-b + sqrt(D)) / 2a and right limit x2 = (-b - sqrt(D)) / 2a
#
# because the distances are mirrored around the center point we could simplify this by using one limit
# and calculating from that limit to the middle and then multiplying by 2
# I didn't implement this because I don't think it will make much of a difference
# if the formula for calculating the limits were more complex (and thus more time consuming) I would consider it


from aoc_2023_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_races,
)

from tools import time_it

from functools import reduce
from operator import mul
from math import sqrt, floor, ceil

from pprint import pprint


# other constants


def calc_limits_for_race(time: int, record: int) -> tuple[float, float]:
    D = time**2 - 4 * (-1) * (-record)
    left_limit = (-time + sqrt(D)) / -2
    right_limit = (-time - sqrt(D)) / -2
    return left_limit, right_limit


@time_it
def main(data_lines: list[str]) -> None:
    races = create_races(data_lines)
    # print(races)

    # loop through all races and remember the number of record-breaking distances
    numbers = []
    for race in races:
        # print(race)

        left_limit, right_limit = calc_limits_for_race(*race)
        # print(left_limit, right_limit)

        # add/subtract a very small number (1e-8) so if any of the limits is exactly equal to the record
        #   the floor and ceiling function will round to the next lower/higher integer
        #   (only distances greater than the record count, not greater than or equal)
        # print(ceil(left_limit + 1e-8), floor(right_limit - 1e-8))
        numbers.append(floor(right_limit - 1e-8) - ceil(left_limit + 1e-8) + 1)
        # print(floor(right_limit - 1e-8) - ceil(left_limit + 1e-8) + 1)

        # print('-' * 100)

    # print(numbers)

    # multiply all numbers for the end result
    print(f'End result: {reduce(mul, numbers, 1)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 288
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 2344708
    #   Finished 'main' in less than a millisecond

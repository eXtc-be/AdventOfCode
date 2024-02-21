# aoc_2017_03_A_1.py - Day 3: Spiral Memory - part 1
# How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?
# https://adventofcode.com/2017/day/3


from tools import time_it

from typing import NamedTuple
from math import sqrt

from pprint import pprint


DATA_PATH = './input_2017_03'

# other constants


class Point(NamedTuple):
    x: int
    y: int


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def manhattan(start_node: Point, stop_node: Point = Point(0, 0)) -> int:  # return Manhattan distance between start_node and stop_node
    return abs(start_node.x - stop_node.x) + abs(start_node.y - stop_node.y)


def get_distance(number: int) -> int:
    base = int(sqrt(number))
    base -= (base-1) % 2  # make sure base is odd
    corner_value = base * base
    row = col = base // 2
    arm_length = (base // 2 + 1) * 2

    # perfect square
    if number == corner_value:
        return manhattan(Point(row, col))

    # update row, column and corner value for start of 1st arm (lower right)
    col += 1
    corner_value += 1
    if number < corner_value + arm_length:
        return manhattan(Point(col, row - (number - corner_value)))

    # update column and corner value for start of 2nd arm (upper right)
    row -= arm_length - 1
    col -= 1
    corner_value += arm_length
    if number < corner_value + arm_length:
        return manhattan(Point(col - (number - corner_value), row))

    # update column and corner value for start of 3rd arm (upper left)
    col -= arm_length - 1
    row += 1
    corner_value += arm_length
    if number < corner_value + arm_length:
        return manhattan(Point(col, row + (number - corner_value)))

    # update column and corner value for start of 4th arm (lower left)
    row += arm_length - 1
    col += 1
    corner_value += arm_length
    if number < corner_value + arm_length:
        return manhattan(Point(col + (number - corner_value), row))


test_data = '''
1
12
17
20
23
1024
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, get_distance(int(line)))

    print(f'End result: {get_distance(int(data_lines[0]))}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 0, 3, 4, 3, 2, 31
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 480
    #   Finished 'main' in less than a millisecond

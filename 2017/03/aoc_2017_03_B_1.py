# aoc_2017_03_B_1.py - Day 3: Spiral Memory - part 2
# What is the first value written that is larger than your puzzle input?
# https://adventofcode.com/2017/day/3


from aoc_2017_03_A_1 import (
    DATA_PATH,
    load_data, Point,
    # test_data,
)

from tools import time_it

from typing import NamedTuple
from itertools import cycle

from pprint import pprint


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


DIRECTIONS = [
    Point(1, 0),  # R
    Point(0, -1),  # U
    Point(-1, 0),  # L
    Point(0, 1),  # D
]

NEIGHBOURS = [
    Point(-1, -1),
    Point(0, -1),
    Point(1, -1),
    Point(-1, 0),
    Point(1, 0),
    Point(-1, 1),
    Point(0, 1),
    Point(1, 1),
]


def _get_number(grid: dict[Point, int], point: Point) -> int:
    # total = 0
    # for neighbor in NEIGHBOURS:
    #     if point + neighbor in grid:
    #         total += grid[point + neighbor]
    #
    return sum(grid[point + neighbor] for neighbor in NEIGHBOURS if point + neighbor in grid)


def get_numbers(threshold: int) -> int:
    directions = cycle(DIRECTIONS)  # re-initialize directions cycler every time the function is called

    last_num = 1
    last_point = Point(0, 0)

    grid = {last_point: last_num}

    index = 0
    while True:
        d = next(directions)
        for _ in range(index // 2 + 1):
            last_point += d
            # last_num += 1
            last_num = _get_number(grid, last_point)
            grid[last_point] = last_num
            if last_num > threshold:
                return last_num
        index += 1


def print_grid(grid: dict[Point, int]) -> None:
    width = len(f'{max(grid.values())}')

    y_min = min(p.y for p in grid)
    y_max = max(p.y for p in grid)
    x_min = min(p.x for p in grid)
    x_max = max(p.x for p in grid)

    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if Point(x, y) in grid:
                print(f'{grid[Point(x, y)]:0{width}}', end=' ')
            else:
                print('_' * width, end=' ')
        print()


test_data = '''
4
23
54
147
806
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # num = get_numbers(747)
    # print(num)

    # for line in data_lines:
    #     print(line, get_numbers(int(line)))

    print(f'End result: {get_numbers(int(data_lines[0]))}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 5, 25, 57, 304, 880
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 349975
    #   Finished 'main' in 1 millisecond

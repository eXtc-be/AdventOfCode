# aoc_2018_06_B_1.py - Day 6: Chronal Coordinates - part 2
# What is the size of the region containing all locations
# which have a total distance to all given coordinates of less than 10000?
# https://adventofcode.com/2018/day/6


from aoc_2018_06_A_1 import (
    DATA_PATH,
    Point,
    NamedPoint,
    load_data,
    test_data,
    get_coords,
    # populate_grid,
)

from tools import time_it

# other imports

from pprint import pprint


MAX_SUM = 10_000
MAX_SUM_TEST = 32


def _get_sum(coords: list[NamedPoint], point: Point) -> int:
    return sum(coord.location.distance(point) for coord in coords)


def get_region(coords: list[NamedPoint], max_sum: int = MAX_SUM) -> dict[Point, int]:
    region = {}
    for row in range(max(coord.location.y for coord in coords) + 2):
        for col in range(max(coord.location.x for coord in coords) + 2):
            total = _get_sum(coords, Point(col, row))
            if total < max_sum:
                region[Point(row, col)] = total

    return region

@time_it
def main(data_lines: list[str], max_sum: int = MAX_SUM) -> None:
    coords = get_coords(data_lines)
    # pprint(coords)

    region = get_region(coords, max_sum)
    # pprint(region)

    print(f'End result: {len(region)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, MAX_SUM_TEST)
    # using test_data:
    #   End result: 16
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 45176
    #   Finished 'main' in 1.51 seconds

# aoc_2019_10_A_2.py - Day 10: Monitoring Station - part 1
# Find the best location for a new monitoring station.  How many other asteroids can be detected from that location?
# https://adventofcode.com/2019/day/10
# this version uses math.atan2 to calculate the angle between points
# we no longer need to consider quadrants, and points can easily be sorted by angle


from aoc_2019_10_A_1 import (
    DATA_PATH,
    Point,
    load_data,
    get_points,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint

# other constants


def points_visible(points: list[Point], p1: Point) -> int:
    return len({p1.angle(p2) for p2 in points if p2 != p1})


@time_it
def main(data_lines: list[str]) -> None:
    points = get_points(data_lines)
    # pprint(points)

    print(f'End result: {max(points_visible(points, point) for point in points)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])

    # using test_data 0:
    #   End result: 8
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 33
    #   Finished 'main' in 2 milliseconds
    # using test_data 2:
    #   End result: 35
    #   Finished 'main' in 2 milliseconds
    # using test_data 3:
    #   End result: 41
    #   Finished 'main' in 2 milliseconds
    # using test_data 4:
    #   End result: 210
    #   Finished 'main' in 108 milliseconds
    # using input data:
    #   End result: 303
    #   Finished 'main' in 158 milliseconds

# aoc_2019_10_A_2.py - Day 10: Monitoring Station - part 1
# Find the best location for a new monitoring station.  How many other asteroids can be detected from that location?
# https://adventofcode.com/2019/day/10
# this version also uses y = m * x + q, but only to calculate the slope between pairs of points
# it then counts unique slopes in each quadrant as the number of points visible from a given point


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
    slopes_q1 = set()  # upper right
    slopes_q2 = set()  # lower right
    slopes_q3 = set()  # lower left
    slopes_q4 = set()  # upper left

    for p2 in points:
        if p1 != p2:
            if p1.x <= p2.x and p1.y > p2.y:    # upper right
                slopes_q1.add(p1.slope(p2))
            elif p1.x < p2.x and p1.y <= p2.y:  # lower right
                slopes_q2.add(p1.slope(p2))
            elif p1.x >= p2.x and p1.y < p2.y:  # lower left
                slopes_q3.add(p1.slope(p2))
            elif p1.x > p2.x and p1.y >= p2.y:  # upper left
                slopes_q4.add(p1.slope(p2))

    return sum(len(s) for s in (slopes_q1, slopes_q2, slopes_q3, slopes_q4))


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
    #   Finished 'main' in 1 millisecond
    # using test_data 3:
    #   End result: 41
    #   Finished 'main' in 2 milliseconds
    # using test_data 4:
    #   End result: 210
    #   Finished 'main' in 80 milliseconds
    # using input data:
    #   End result: 303
    #   Finished 'main' in 131 milliseconds

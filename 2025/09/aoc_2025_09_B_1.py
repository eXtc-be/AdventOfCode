# aoc_2025_09_B_1.py - Day 9: Movie Theater - part 2
# Using two red tiles as opposite corners, what is the largest area of any
# rectangle you can make using only red and green tiles?
# https://adventofcode.com/2025/day/9

from aoc_2025_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_points,
    Point,
)

from tools import time_it

# other imports

from pprint import pprint
from itertools import combinations
from functools import cache


# other constants


# other functions
@cache
def point_inside(point: Point) -> bool:
    global min_x, points, horizontals, verticals

    # check if the point is one of the other points
    if point in points:
        return True

    # check if the point is on one of the horizontal lines (except points)
    for horizontal in horizontals:
        if horizontal[0].x < point.x < horizontal[1].x and point.y == horizontal[0].y:
            return True

    # check if the point is on one of the vertical lines (except points)
    for vertical in verticals:
        if vertical[0].y < point.y < vertical[1].y and point.x == vertical[0].x:
            return True

    # count the number of verticals crossed between min_x and point.x
    vertical_crossings = [
        vertical for vertical in verticals
        if min_x <= vertical[0].x < point.x and vertical[0].y <= point.y < vertical[1].y
    ]

    # if the number of crossings is odd, the point is inside the polygon
    if len(vertical_crossings) % 2 == 1:
        return True

    return False


@cache
def line_inside(start: Point, end: Point) -> bool:
    if start == end:
        return point_inside(start)
    else:
        if point_inside(start) and point_inside(end):
            if start.x == end.x:  # vertical
                return (line_inside(start, Point(start.x, start.y + (end.y - start.y) // 2))
                        and line_inside(Point(start.x, start.y + (end.y - start.y) // 2 + 1), end))
            elif start.y == end.y:  # horizontal
                return (line_inside(start, Point(start.x + (end.x - start.x) // 2, start.y))
                        and line_inside(Point(start.x + (end.x - start.x) // 2 + 1, start.y), end))
            else:
                raise ValueError('no diagonal lines!')
        else:
            return False


@cache
def rectangle_inside(first: Point, second: Point) -> bool:
    global min_x, points, horizontals, verticals

    # opposite corners must also be points in the set
    if not point_inside(Point(second.x, first.y)) or not point_inside(Point(first.x, second.y)):
        return False

    # make sure the first point's x-coordinate is smaller than the second's
    if first.x > second.x:
        first, second = second, first

    # verify if both horizontal sides of the rectangle are inside the polygon
    for h_side in (first, Point(second.x, first.y)), (Point(first.x, second.y), second):
        if not line_inside(*h_side):
            return False

    # make sure the first point's y-coordinate is smaller than the second's
    if first.y > second.y:
        first, second = second, first

    # verify if both vertical sides of the rectangle are inside the polygon
    for v_side in (first, Point(first.x, second.y)), (Point(second.x, first.y), second):
        if not line_inside(*v_side):
            return False

    # all tests passed, so rectangle must be completely inside the polygon
    return True


@time_it
def main(data_lines: list[str]) -> None:
    global min_x, points, horizontals, verticals

    points = get_points(data_lines)

    min_x = min(point.x for point in points)

    # make a list of all horizontal lines (and sort their points by x)
    horizontals = [
        (sorted(pair, key=lambda c: c.x))
        for pair in zip(points, points[1:] + [points[0]])
        if pair[0].y == pair[1].y
    ]

    # make a list of all vertical lines (and sort their points by y)
    verticals = [
        (sorted(pair, key=lambda c: c.y))
        for pair in zip(points, points[1:] + [points[0]])
        if pair[0].x == pair[1].x
    ]

    result = 0
    combos = sorted(
        combinations(points, 2),
        key=lambda c: (abs(c[1].x - c[0].x) + 1) * (abs(c[1].y - c[0].y) + 1),
        reverse=True
    )
    for first, second in combos:
        print(first, second, (abs(second.x - first.x) + 1) * (abs(second.y - first.y) + 1))
        if rectangle_inside(first, second):
            result = (abs(second.x - first.x) + 1) * (abs(second.y - first.y) + 1)
            break

    print(f'End result: {result}')


test_data_2 = '''
7,1
11,1
11,7
9,7
9,5
4,5
4,6
2,6
2,3
7,3
'''.strip().splitlines()


if __name__ == "__main__":
    global min_x, points, horizontals, verticals

    main(load_data(DATA_PATH))
    # main(test_data)
    # main(test_data_2)

    # using test_data:
    #   End result: 24
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4652231070 -- too high
    #   Finished 'main' in 5.0 seconds
    #   End result: 2451913560 -- too high
    #   Finished 'main' in 7.5 seconds
    #   End result: 1544362560
    #   Finished 'main' in 42 minutes and 18 seconds
    #   End result: 1544362560
    #   Finished 'main' in 30 minutes and 29 seconds -- after optimization: first check size, then if inside
    #   End result: 1544362560
    #   Finished 'main' in 16 minutes and 49 seconds -- after optimization: first check opposite corners
    #   End result: 1544362560
    #   Finished 'main' in 13 minutes and 54 seconds -- after optimization: generate all rectangles and sort
    #                                                   by size (largest first), stop after first positive test
    #   End result: 1544362560
    #   Finished 'main' in 12 minutes and 16 seconds -- after optimization: rewrote line_inside

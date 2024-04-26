# aoc_2019_10_A_1.py - Day 10: Monitoring Station - part 1
# Find the best location for a new monitoring station.  How many other asteroids can be detected from that location?
# https://adventofcode.com/2019/day/10
# this version uses y = m * x + q to calculate all points between a pair of points
# and counts the number of points that are not obstructed by another point
# using sets and intersection instead of lists and 'in' made this twice as fast,
# unfortunately it doesn't yield the correct answer


from tools import time_it

from dataclasses import dataclass
from sys import maxsize
from math import atan2, pi, radians, degrees

from pprint import pprint


DATA_PATH = './input_2019_10'

EMPTY = '.'
ASTEROID = '#'


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def slope(self, other: 'Point') -> float:
        if self.x == other.x:
            return maxsize
        return (self.y - other.y) / (other.x - self.x)


    def angle(self, other: 'Point') -> float:
        # pi/2 - atan -> reverse direction and shift 90°
        # (self.y-other.y)/(other.x-self.x) -> y grows going down
        angle = pi/2 - atan2((self.y - other.y), (other.x - self.x))
        if angle < 0:  # atan returns angle between pi and -pi
            angle += pi * 2  # add 2 pi to return angle between 0 and 2 pi
        return degrees(angle)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_points(data_lines: list[str]) -> list[Point]:
    return [
        Point(int(c), int(r))
        for r, row in enumerate(data_lines) for c, char in enumerate(row)
        if char == ASTEROID
    ]


def points_on_line(p1: Point, p2: Point) -> list[Point]:
    if p1.x == p2.x:
        y1, y2 = sorted((p1.y, p2.y))
        return [Point(p1.x, y) for y in range(y1 + 1, y2)]
    elif p1.y == p2.y:
        x1, x2 = sorted((p1.x, p2.x))
        return [Point(x, p1.y) for x in range(x1 + 1, x2)]
    else:
        m = (p2.y - p1.y) / (p2.x - p1.x)
        q = p1.y - p1.x * m
        x1, x2 = sorted((p1.x, p2.x))
        return [Point(x, int(m * x + q)) for x in range(x1 + 1, x2) if m * x + q == int(m * x + q)]


def points_visible(points: set[Point], p1: Point) -> int:
    visible = 0

    for p2 in points:
        if p1 != p2:
            # if not any(p in points for p in points_on_line(p1, p2)):
            if not points.intersection(points_on_line(p1, p2)):
                visible += 1

    return visible


test_data = [
'''
.#..#
.....
#####
....#
...##
'''.strip().splitlines(),
'''
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
'''.strip().splitlines(),
'''
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
'''.strip().splitlines(),
'''
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
'''.strip().splitlines(),
'''
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''.strip().splitlines(),
]


@time_it
def main(data_lines: list[str]) -> None:
    points = get_points(data_lines)
    # pprint(points)

    # for point in points:
    #     print(point, points_visible(points, point))

    print(f'End result: {max(points_visible(set(points), point) for point in points)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])

    # using test_data 0:
    #   End result: 8
    #   Finished 'main' in 1 millisecond
    # using test_data 1:
    #   End result: 33
    #   Finished 'main' in 14 milliseconds
    # using test_data 2:
    #   End result: 35
    #   Finished 'main' in 14 milliseconds
    # using test_data 3:
    #   End result: 41
    #   Finished 'main' in 22 milliseconds
    # using test_data 4:
    #   End result: 214 - too high
    #   Finished 'main' in 2.3 seconds
    # using input data:
    #   End result: 306 - too high
    #   Finished 'main' in 7.8 seconds

    # test points_on_line
    # print(points_on_line(Point(1, 1), Point(1, 10)))   # vertical line
    # print(points_on_line(Point(1, 1), Point(10, 1)))   # horizontal line
    # print(points_on_line(Point(1, 1), Point(10, 10)))  # diagonal line positive slope
    # print(points_on_line(Point(1, 1), Point(10, 5)))   # diagonal line positive slope
    # print(points_on_line(Point(1, 1), Point(5, 10)))   # diagonal line positive slope
    # print(points_on_line(Point(1, 10), Point(10, 1)))  # diagonal line negative slope

    # test points_on_line with actual data
    # points = get_points(test_data)
    # print(points[0], points[-2], points_on_line(points[0], points[-2]))
    # print(points[0], points[-1], points_on_line(points[0], points[-1]))
    # print(points[2], points[6], points_on_line(points[2], points[6]))
    # print(points[2], points[-1], points_on_line(points[2], points[-1]))

    # # test Point.angle
    # print(f'{Point(4, 4).angle(Point(4, 0)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(8, 0)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(8, 4)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(8, 8)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(4, 8)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(0, 8)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(0, 4)):-4.0f}')
    # print(f'{Point(4, 4).angle(Point(0, 0)):-4.0f}')

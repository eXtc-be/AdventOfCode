# aoc_2019_10_B_1.py - Day 10: Monitoring Station - part 2
# Which will be the 200th asteroid to be vaporized?
# https://adventofcode.com/2019/day/10
# using the angles from aoc_2019_10_A_3.py, this version removes asteroids as requested in the correct order


import sys
sys.path.extend(['.', '..', '../..'])


from aoc_2019_10_A_1 import (
    DATA_PATH,
    Point,
    load_data,
    get_points,
    # test_data,
)

from aoc_2019_10_A_3 import (
    points_visible,
)

from tools import time_it, clear

from collections import defaultdict

from pprint import pprint


TARGET_NUM = 200


def print_points(points: list[Point], width: int, height: int, origin: Point = None, target: Point = None) -> None:
    for r in range(height):
        for c in range(width):
            if Point(c, r) in points:
                if origin and Point(c, r) == origin:
                    print('X', end='')
                elif target and Point(c, r) == target:
                    print('*', end='')
                else:
                    print('#', end='')
            else:
                print('.', end='')
        print()


def remove_points(points: list[Point], origin: Point = None, target_num: int = TARGET_NUM) -> Point:
    counter = 0
    target = None

    # get width and height for complete set of points, so print_points is always the same dimensions
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)

    # group points by angle
    groups = defaultdict(list)
    for point in points:
        if point != origin:
            groups[origin.angle(point)].append(point)

    while len(points) > 1:
        for angle, group in sorted(groups.items(), key=lambda x: x[0]):  # sort groups by angle
            if group:  # group still has points
                target = sorted(group, key=lambda p: origin.distance(p))[0]  # sort each sublist by distance

                clear()
                print(counter, target)
                print('-' * 100)
                print_points(points, max_x+1, max_y+1, origin, target)
                input()

                points.remove(target)
                groups[angle].remove(target)

                counter += 1
                if counter >= target_num:
                    return target


test_data = [
'''
#...#...#
.........
.........
.........
#...#...#
.........
.........
.........
#...#...#
'''.strip().splitlines(),
'''
....#...#
.........
.........
........#
....##..#
.......#.
.........
.........
....#....
'''.strip().splitlines(),
'''
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
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

    best = max([(point, points_visible(points, point)) for point in points], key=lambda p: p[1])[0]
    # print(best)
    # print_points(points, best, Point(8, 1))

    # target = remove_points(points, Point(4, 4), 15)
    target = remove_points(points, best)
    # print(target)

    print(f'End result: {target.x *100 + target.y if target else "None"}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])

    # using test_data 3:
    #   End result: 802
    #   Finished 'main' in 111 milliseconds
    # using input data:
    #   End result: 408
    #   Finished 'main' in 169 milliseconds

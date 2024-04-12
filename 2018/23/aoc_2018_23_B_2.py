# aoc_2018_23_B_2.py - Day 23: Experimental Emergency Teleportation - part 2
# Find the coordinates that are in range of the largest number of nanobots.
# What is the shortest manhattan distance between any of those points and 0,0,0?
# https://adventofcode.com/2018/day/23
# new strategy: divide the encompassing rectangle into 8 equal (+/- 1) sub rectangles;
#   count the bots in every sub rectangle and put each one on a priority queue
#   along with this count and the distance from its center to the origin;
#   keep dividing rectangles until both corners are equal (a point)


from aoc_2018_23_A_1 import (
    DATA_PATH,
    Point,
    Bot,
    load_data,
    get_bots,
    # test_data,
)

from tools import time_it

import heapq

from pprint import pprint


# other constants


def divide_cube(p_1: Point, p_2: Point) -> list[tuple[Point, Point]]:
    """divides the cube defined by p_1 and p_2 into 8 equal (+/- 1) parts"""
    m_x = (p_2.x - p_1.x) // 2
    m_y = (p_2.y - p_1.y) // 2
    m_z = (p_2.z - p_1.z) // 2

    if m_x == m_y == m_z == 0:  # difference between coordinate pairs <= 1
        return [(p_1, p_1), (p_2, p_2)]
    else:
        return [
            (
                Point(p_1.x + x * m_x, p_1.y + y * m_y, p_1.z + z * m_z),
                Point(p_2.x - (1-x) * m_x, p_2.y - (1-y) * m_y, p_2.z - (1-z) * m_z)
            )
            for x in range(2) for y in range(2) for z in range(2)
        ]


def count_bots(bots: list[Bot], p_1: Point, p_2: Point) -> int:
    """returns the number of bots that are in range of the cube defined by p_1 and p_2"""
    return len([bot for bot in bots if bot.in_cube(p_1, p_2)])


def cube_distance(p_1: Point, p_2: Point) -> int:
    """returns the Manhattan distance from the center of a cube defined by p_1 and p_2 to the origin"""
    return p_1.x + (p_2.x - p_1.x) // 2 + p_1.y + (p_2.y - p_1.y) // 2 + p_1.z +(p_2.z - p_1.z) // 2


test_data = '''
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<10,10,10>, r=5
'''.strip().splitlines()

# test_data = '''
# pos=<10,12,12>, r=2
# pos=<12,14,12>, r=2
# pos=<16,12,12>, r=4
# pos=<14,14,14>, r=6
# pos=<10,10,10>, r=5
# '''.strip().splitlines()

# test_data = '''
# pos=<10,12,12>, r=2
# pos=<12,14,12>, r=2
# pos=<16,12,12>, r=4
# pos=<14,14,14>, r=6
# pos=<50,50,50>, r=200
# pos=<10,10,10>, r=5
# '''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    bots = get_bots(data_lines)

    min_x = min([bot.loc.x for bot in bots])
    min_y = min([bot.loc.y for bot in bots])
    min_z = min([bot.loc.z for bot in bots])
    max_x = max([bot.loc.x for bot in bots])
    max_y = max([bot.loc.y for bot in bots])
    max_z = max([bot.loc.z for bot in bots])
    # min_x = min([bot.loc.x - bot.r for bot in bots])
    # min_y = min([bot.loc.y - bot.r for bot in bots])
    # min_z = min([bot.loc.z - bot.r for bot in bots])
    # max_x = max([bot.loc.x + bot.r for bot in bots])
    # max_y = max([bot.loc.y + bot.r for bot in bots])
    # max_z = max([bot.loc.z + bot.r for bot in bots])
    # print(min_x, min_y, min_z, '-', max_x, max_y, max_z)

    current_cube = Point(min_x, min_y, min_z), Point(max_x, max_y, max_z)
    num = count_bots(bots, *current_cube)
    dist = cube_distance(*current_cube)
    queue = [(-num, dist, *current_cube)]
    while queue:
        num, dist, *current_cube = heapq.heappop(queue)
        if num == 0:
            continue  # skip cubes without any bots in range
        if current_cube[0].distance(current_cube[1]) == 0:
            break
        else:
            for cube in divide_cube(*current_cube):
                heapq.heappush(queue, (-count_bots(bots, *cube), cube_distance(*cube), *cube))

    print(num, dist, *current_cube)

    print(f'End result: {dist}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

    # pprint(divide_cube(0, 0, 0, 15, 15, 15,))
    # pprint(divide_cube(0, 0, 0, 1, 1, 1,))

    # from aoc_2018_23_A_1 import Bot
    # print(Bot(5, 5, 5, 3).in_cube(0, 0, 0, 10, 10, 10))  # True - completely inside cube
    # print(Bot(5, 5, 5, 20).in_cube(0, 0, 0, 10, 10, 10))  # True - completely engulfing cube
    # print(Bot(5, 5, 15, 3).in_cube(0, 0, 0, 10, 10, 10))  # False - outside cube, too small
    # print(Bot(5, 5, 15, 10).in_cube(0, 0, 0, 10, 10, 10))  # True - outside cube, big enough
    # print(Bot(100000009, 100000000, 0, 10).in_cube(0, 0, 0, 100000000, 100000000, 0))  # True - barely touching cube
    # print(Bot(110000000, 110000000, 0, 10).in_cube(0, 0, 0, 100000000, 100000000, 0))  # False - at corner, not touching
    # print(Bot(100000008, 100000008, 0, 10).in_cube(0, 0, 0, 100000000, 100000000, 0))  # True - at corner, touching

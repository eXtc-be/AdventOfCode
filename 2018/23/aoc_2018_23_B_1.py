# aoc_2018_23_B_1.py - Day 23: Experimental Emergency Teleportation - part 2
# Find the coordinates that are in range of the largest number of nanobots.
# What is the shortest manhattan distance between any of those points and 0,0,0?
# https://adventofcode.com/2018/day/23
# naive strategy: for every point in the encompassing cube count the number of bots in range;
#   keep the one with the most bots in range; for ties choose the one closest to the origin
#   this solves the example in 276 milliseconds, but will take 500_000_000 ** 3 times longer for the real data


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


# other functions


test_data = '''
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    bots = get_bots(data_lines)

    min_x = min([bot.loc.x for bot in bots])
    min_y = min([bot.loc.y for bot in bots])
    min_z = min([bot.loc.z for bot in bots])
    max_x = max([bot.loc.x for bot in bots])
    max_y = max([bot.loc.y for bot in bots])
    max_z = max([bot.loc.z for bot in bots])

    max_bots, dist, p = 0, 0, None
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z+1):
                point = Point(x, y, z)
                in_range = len([bot for bot in bots if bot.in_range(point)])
                if in_range > max_bots or in_range == max_bots and point.distance() < dist:
                    max_bots = in_range
                    dist = point.distance()
                    p = point

    print(max_bots, dist, p)

    print(f'End result: {dist}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 36 (5 bots in range of Point(x=12, y=12, z=12))
    #   Finished 'main' in 276 milliseconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

    # bots = get_bots(test_data)
    # point = Point(12, 12, 12)
    # print([bot for bot in bots if bot.in_range(point)])

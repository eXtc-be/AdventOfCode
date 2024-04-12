# aoc_2018_23_B_4.py - Day 23: Experimental Emergency Teleportation - part 2
# Find the coordinates that are in range of the largest number of nanobots.
# What is the shortest manhattan distance between any of those points and 0,0,0?
# https://adventofcode.com/2018/day/23
# instead of dividing coordinates, this version uses decreasing step sizes to
#   minimize the number of coordinates to check


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


@time_it
def main(data_lines: list[str]) -> None:
    bots = get_bots(data_lines)

    min_x = min([bot.loc.x for bot in bots])
    min_y = min([bot.loc.y for bot in bots])
    min_z = min([bot.loc.z for bot in bots])
    max_x = max([bot.loc.x for bot in bots])
    max_y = max([bot.loc.y for bot in bots])
    max_z = max([bot.loc.z for bot in bots])
    print(min_x, min_y, min_z, '-', max_x, max_y, max_z)

    delta_x = max_x - min_x
    delta_y = max_y - min_y
    delta_z = max_z - min_z

    offset = Point(min_x, min_y, min_z)

    for factor in range(8):
        step_x = delta_x // 10 ** (factor + 1)
        step_y = delta_y // 10 ** (factor + 1)
        step_z = delta_z // 10 ** (factor + 1)

        max_bots, dist, winner = 0, 0, None

        for x in range(offset.x + step_x // 2, offset.x + 10 * step_x + step_x // 2, step_x):
            for y in range(offset.y + step_y // 2, offset.y + 10 * step_y + step_y // 2, step_y):
                for z in range(offset.z + step_z // 2, offset.z + 10 * step_z + step_z // 2, step_z):
                    point = Point(x, y, z)
                    in_range = len([bot for bot in bots if bot.in_range(point)])
                    if in_range > max_bots or in_range == max_bots and point.distance() < dist:
                        max_bots = in_range
                        dist = point.distance()
                        winner = point

        print(max_bots, dist, winner)
        offset = winner

    # print(f'End result: {0}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))

    # using input data:
    #   End result: 105,580,102 - too high
    #   Finished 'main' in xxx

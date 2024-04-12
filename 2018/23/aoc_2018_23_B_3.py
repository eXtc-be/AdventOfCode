# aoc_2018_23_B_3.py - Day 23: Experimental Emergency Teleportation - part 2
# Find the coordinates that are in range of the largest number of nanobots.
# What is the shortest manhattan distance between any of those points and 0,0,0?
# https://adventofcode.com/2018/day/23
# based on reddit user timrprobocom's solution
# (https://old.reddit.com/r/adventofcode/comments/19beeg7/2018_day_23_part_2_python/kiuvo4g/)
# divide all bot coordinates by 100 million (they range from about -300 million to about +200 million)
#   and find the point with the most bots in range by checking each point individually
#   (the field is now reduced to 10 x 10 x 10)
#   then do the next pass with all coordinates divided by 10 million and an offset based on the previous result
#   do this until the divisor is 1
#   in total there should be 9 * 1000 checks instead of 500 million cubed


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
    offset = Point(0, 0, 0)

    for factor in range(8):
        multiplier = 10 ** factor
        divisor = 10 ** (8 - factor)

        bots = get_bots(data_lines, divisor)

        min_x = min([bot.loc.x for bot in bots])
        min_y = min([bot.loc.y for bot in bots])
        min_z = min([bot.loc.z for bot in bots])
        max_x = max([bot.loc.x for bot in bots])
        max_y = max([bot.loc.y for bot in bots])
        max_z = max([bot.loc.z for bot in bots])
        print(min_x, min_y, min_z, '-', max_x, max_y, max_z)

        x_range = (max_x - min_x) // multiplier
        y_range = (max_y - min_y) // multiplier
        z_range = (max_z - min_z) // multiplier

        max_bots, dist, winner = 0, 0, None
        for x in range(min_x + x_range * offset.x, min_x + x_range * (offset.x + 1)):
            for y in range(min_y + y_range * offset.y, min_y + y_range * (offset.y + 1)):
                for z in range(min_z + z_range * offset.z, min_z + z_range * (offset.z + 1)):
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

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

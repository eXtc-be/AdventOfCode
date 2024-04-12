# aoc_2018_23_B_extern_1.py - Day 23: Experimental Emergency Teleportation - part 2
# Find the coordinates that are in range of the largest number of nanobots.
# What is the shortest manhattan distance between any of those points and 0,0,0?
# https://adventofcode.com/2018/day/23
# based on reddit user EriiKKo's solution
# (https://old.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdqzdg/)


from aoc_2018_23_A_1 import (
    DATA_PATH,
    load_data,
    get_bots,
)

from tools import time_it

from queue import PriorityQueue

from pprint import pprint


# other constants


@time_it
def main(data_lines: list[str]) -> None:
    bots = get_bots(data_lines)

    queue = []
    # queue = PriorityQueue()

    for bot in bots:
        queue.append((max(0, bot.distance() - bot.r), 1))
        queue.append((bot.distance() + bot.r, -1))

    min_dist, max_bots, bot_count = 0, 0, 0

    for distance, diff in sorted(queue):
        bot_count += diff
        if bot_count > max_bots:
            min_dist = distance
            max_bots = bot_count

    # for bot in bots:
    #     queue.put((max(0, bot.distance() - bot.r), 1))
    #     queue.put((bot.distance() + bot.r, -1))
    #
    # min_dist, max_bots, bot_count = 0, 0, 0
    #
    # while not queue.empty():
    #     distance, diff = queue.get()
    #     bot_count += diff
    #     if bot_count > max_bots:
    #         min_dist = distance
    #         max_bots = bot_count

    print(f'End result: {min_dist}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))

    # using input data:
    #   End result: 81396996
    #   Finished 'main' in 16 milliseconds
    #   Finished 'main' in 6 milliseconds with sorted list instead of priority queue

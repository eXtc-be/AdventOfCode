# aoc_2016_24_B_1.py - Day 24: Air Duct Spelunking - part 2
# What is the fewest number of steps required to start at 0, visit every non-0 number
# marked on the map at least once, and then return to 0?
# https://adventofcode.com/2016/day/24


from aoc_2016_24_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_nodes,
    find_sub_path,
    find_path,
)

from tools import time_it

from itertools import combinations

from pprint import pprint


# other constants


# other functions


@time_it
def main(grid: list[str]) -> None:
    # print_grid(grid)

    nodes = get_nodes(grid)
    # print(sorted(nodes))

    # find the shortest path from any node to any other node
    pairs = {s.num: {d.num: 0 for d in nodes} for s in nodes}  # initialize dict of dicts
    for pair in combinations(nodes, 2):
        path = find_sub_path(grid, *[node.loc for node in pair])
        # print_grid(grid, path)
        pairs[pair[0].num][pair[1].num] = len(path)-1
        pairs[pair[1].num][pair[0].num] = len(path)-1
    # pprint(pairs)

    paths = find_path(pairs, loop_back=True)
    # print(paths)

    shortest = sorted(paths, key=lambda p: p[1])[0]
    # print(shortest)

    print(f'End result: {shortest[1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 20
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 804
    #   Finished 'main' in 1.20 seconds

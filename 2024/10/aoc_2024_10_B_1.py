# aoc_2024_10_B_1.py - Day 10: Hoof It - part 2
# What is the sum of the ratings of all trailheads?
# https://adventofcode.com/2024/day/10


from aoc_2024_10_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_map,
    extract_trailheads,
    find_trails
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    topo_map = create_map(data_lines)
    # pprint(topo_map)

    trailheads = extract_trailheads(topo_map)
    # pprint(trailheads)

    result = 0
    for trailhead in trailheads:
        trails = find_trails(topo_map, trailhead)
        # pprint(trails)
        # unique_endpoints = set(trail[-1] for trail in trails)
        # print(len(unique_endpoints))
        # print(len(trails))
        result += len(trails)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 81
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 1722
    #   Finished 'main' in 33 milliseconds

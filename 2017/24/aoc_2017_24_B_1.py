# aoc_2017_24_B_1.py - Day 24: Electromagnetic Moat - part 2
# What is the strength of the longest bridge you can make?
# If you can make multiple bridges of the longest length, pick the strongest one.
# https://adventofcode.com/2017/day/24
# using the decently fast solution from version 4 of part 1, this was trivially simple to solve


from aoc_2017_24_A_4 import (
    DATA_PATH,
    load_data,
    test_data,
    get_components,
    bridge_generator,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    components = get_components(data_lines)
    # pprint(components)

    bridges = list(bridge_generator(None, components))
    # pprint(bridges)

    longest = max(map(len, bridges))
    # print(longest)

    longest_bridges = [bridge for bridge in bridges if len(bridge) == longest]
    # pprint(longest_bridges)

    print(f'End result: {max(sum(sum(port for port in comp) for comp in bridge) for bridge in longest_bridges)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 19
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1471
    #   Finished 'main' in 3.8 seconds

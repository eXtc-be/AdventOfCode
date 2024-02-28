# aoc_2017_19_B_1.py - Day 19: A Series of Tubes - part 2
# How many steps does the packet need to go?
# https://adventofcode.com/2017/day/19


from aoc_2017_19_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_network,
    find_path,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    network = get_network(data_lines)
    # print('\n'.join(row.replace(' ', '.') for row in network))

    path, steps = find_path(network)
    # print(path, steps)

    print(f'End result: {steps}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 38
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 17302
    #   Finished 'main' in 16 milliseconds

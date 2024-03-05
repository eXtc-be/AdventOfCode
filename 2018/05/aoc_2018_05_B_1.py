# aoc_2018_05_B_1.py - Day 5: Alchemical Reduction - part 2
# What is the length of the shortest polymer you can produce by removing all units
# of exactly one type and fully reacting the result?
# https://adventofcode.com/2018/day/5


from aoc_2018_05_A_2 import (
    DATA_PATH,
    load_data,
    test_data,
    reduce,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data: str) -> None:
    shortest = len(data)

    for removed in set(data.lower()):
        a = data.replace(removed, '').replace(removed.upper(), '')
        # print(removed)
        # print(removed, a)
        reduced = reduce(a)
        # print(reduced, len(reduced))
        if len(reduced) < shortest:
            shortest = len(reduced)

    print(f'End result: {shortest}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4178
    #   Finished 'main' in 192 milliseconds

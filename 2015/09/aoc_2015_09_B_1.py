# aoc_2015_09_B_1.py - Day 9: All in a Single Night - part 2
# What is the distance of the shortest route?
# https://adventofcode.com/2015/day/9


from aoc_2015_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_map,
    get_distances
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    map = get_map(data_lines)
    # pprint(map)

    distances = get_distances(map)
    # pprint(distances)

    longest = sorted(distances, key=lambda d: d[1])[-1]
    print(f'End result: {" -> ".join(longest[0])} = {longest[1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: Belfast -> London -> Dublin = 982
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: Snowdin -> Tambi -> Norrath -> AlphaCentauri -> Straylight -> Arbre -> Faerun -> Tristram = 898
    #   Finished 'main' in 91 milliseconds

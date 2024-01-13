# aoc_2015_13_B_1.py - Day 13: Knights of the Dinner Table - part 2
# What is the total change in happiness for the optimal seating arrangement of the guest list plus one?
# https://adventofcode.com/2015/day/13


from aoc_2015_13_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_map,
    get_happinesss
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def add_guest(new_guest, score, map: dict[str: dict[str, int]]) -> dict[str: dict[str, int]]:
    my_map = {}
    for guest, others in map.items():
        others[new_guest] = score
        my_map[guest] = score
    map[new_guest] = my_map


@time_it
def main(data_lines: list[str]) -> None:
    map = get_map(data_lines)
    # pprint(map)

    # pprint(list(permutations(map, r=len(map))))

    add_guest('Chris', 0, map)
    # pprint(map)

    happiness = get_happinesss(map)
    # pprint(happiness)

    happiest = sorted(happiness, key=lambda d: d[1])[-1]
    print(f'End result: {" -> ".join(happiest[0] + happiest[0][0:1])} = {happiest[1]}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 286
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 640
    #   Finished 'main' in 1 second

# aoc_2023_05_B_1.py - Day 5: If You Give A Seed A Fertilizer - part 2
# What is the lowest location number that corresponds to any of the initial seed numbers,
# if you take into account that the individual seed numbers on the first line are actually ranges?
# https://adventofcode.com/2023/day/5
# rewritten find_locations from aoc_2023_05_A_2 to account for the fact that the numbers on the first line are ranges


from aoc_2023_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from aoc_2023_05_A_2 import (
    maps,
    generate_maps,
    _calc_destination,
    _map_x_to_y
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def find_locations(seed_line: str):
    """rewrite of the original function for pairs of seeds/number in the seed line instead of seed numbers"""
    seed_values = seed_line.split()[1:]
    locations = []
    for seed_start, seed_num in zip(seed_values[0::2], seed_values[1::2]):
        # print(seed_start, seed_num)
        for seed in range(int(seed_start), int(seed_start) + int(seed_num)):
            locations.append(_map_x_to_y('seed', 'location', seed))
    return locations


@time_it
def main(data_lines: list[str]) -> None:
    generate_maps(data_lines)
    # pprint(maps)

    locations = find_locations(data_lines[0])
    # print(locations)
    # with test_data this should give:
    # [82, 83, 84, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 60, 86, 87, 88, 89, 94, 95, 96, 56, 57, 58, 59, 97, 98]
    print(f'End result: {min(locations)}')  # should be 46 for test_data


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 46
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: ???
    #   Didn't finish 'main' (takes too long)

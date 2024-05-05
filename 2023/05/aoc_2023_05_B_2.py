# aoc_2023_05_B_2.py - Day 5: If You Give A Seed A Fertilizer - part 2
# What is the lowest location number that corresponds to any of the initial seed numbers,
# if you take into account that the individual seed numbers on the first line are actually ranges?
# https://adventofcode.com/2023/day/5
# in previous versions find_locations keeps all found locations in memory and then finds the smallest value.
# with a dataset of hundreds of millions this could crash the computer, so instead we keep track of
# the lowest value so far (find_lowest_location)


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


def find_lowest_location(seed_line: str) -> int:
    """rewrite of find_locations which returns all locations - this could be a memory problem,
    so instead we keep track of the smallest value so far and forget all calculated values"""
    seed_values = seed_line.split()[1:]
    lowest_location = 0
    for seed_start, seed_num in zip(seed_values[0::2], seed_values[1::2]):
        # print(seed_start, seed_num)
        for seed in range(int(seed_start), int(seed_start) + int(seed_num)):
            location = _map_x_to_y('seed', 'location', seed)
            if not lowest_location or location < lowest_location:
                lowest_location = location
    return lowest_location


@time_it
def main(data_lines: list[str]) -> None:
    generate_maps(data_lines)
    # pprint(maps)

    lowest_location = find_lowest_location(data_lines[0])

    print(f'End result: {lowest_location}')  # should be 46 for test_data


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 46
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: ???
    #   Didn't finish 'main' (takes too long)

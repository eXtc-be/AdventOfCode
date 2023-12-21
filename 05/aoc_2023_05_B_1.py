# aoc_2023_05_B_1.py - Day 5: If You Give A Seed A Fertilizer - part 2
# build translation maps from text file and use them to find locations
# instead of just a list of seed numbers, the seed line must now be considered containing pairs of numbers,
# the first in the pair being the start number, the second one the number of seeds
# the previous version (find_locations) keeps all found locations in memory and then finds the smallest value
# with a dataset of hundreds of millions this could crash the computer, so instead we keep track of
# the lowest value so far (find_lowest_location)
# https://adventofcode.com/2023/day/5


from aoc_2023_05_A_2 import (
    DATA_PATH,
    load_data,
    test_data,
    maps,
    generate_maps,
    _calc_destination,
    _map_x_to_y
)

from pprint import pprint


def find_locations(seed_line):
    """rewrite of the original function for pairs of seeds/number in the seed line instead of seed numbers"""
    seed_values = seed_line.split()[1:]
    locations = []
    for seed_start, seed_num in zip(seed_values[0::2], seed_values[1::2]):
        print(seed_start, seed_num)
        for seed in range(int(seed_start), int(seed_start) + int(seed_num)):
            locations.append(_map_x_to_y('seed', 'location', seed))
    return locations


def find_lowest_location(seed_line):
    """rewrite of find_locations which returns all locations - this could be a memory problem,
    so instead we keep track of the smallest value so far and forget all calculated values"""
    seed_values = seed_line.split()[1:]
    lowest_location = 0
    for seed_start, seed_num in zip(seed_values[0::2], seed_values[1::2]):
        print(seed_start, seed_num)
        for seed in range(int(seed_start), int(seed_start) + int(seed_num)):
            location = _map_x_to_y('seed', 'location', seed)
            if not lowest_location or location < lowest_location:
                lowest_location = location
    return lowest_location


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    generate_maps(data_lines)
    # pprint(maps)

    # test = _map_x_to_y('seed', 'soil', 79)
    # print(f'79 -> {test}')  # should be 81
    # test = _map_x_to_y('seed', 'fertilizer', 14)
    # print(f'14 -> {test}')  # should be 53
    # test = _map_x_to_y('seed', 'water', 55)
    # print(f'55 -> {test}')  # should be 53
    # test = _map_x_to_y('seed', 'location', 13)
    # print(f'13 -> {test}')  # should be 35

    locations = find_locations(data_lines[0])
    print(locations)
    # with test_data this should give:
    # [82, 83, 84, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 60, 86, 87, 88, 89, 94, 95, 96, 56, 57, 58, 59, 97, 98]
    print(f'End result: {min(locations)}')  # should be 46 for test_data

    lowest_location = find_lowest_location(data_lines[0])
    print(f'End result: {lowest_location}')  # should be 46 for test_data

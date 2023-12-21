# aoc_05_B_2.py - Day 5: If You Give A Seed A Fertilizer - part 2
# the list of seed numbers becomes a list of start and amount value pairs
# this version does not calculate the location for every seed in the seed ranges, but instead
# looks at the start number, checks if the source range is smaller than or equal to the destination range
# and calculates only locations for the start and end value for that range; if the source range is bigger,
# it returns destinations for the split off range(s) too
# I did not continue this path, as splitting ranges got complicated real fast
# https://adventofcode.com/2023/day/5


from aoc_05_A_3 import (
    DATA_PATH,
    load_data,
    test_data,
    create_mappings,
    mappings,
)

from pprint import pprint


# def _calc_destination(maps, start, amount):
def _calc_destination(maps, *sources):
    """rewrote to work with ranges instead of individual values"""
    for start, amount in zip(sources[0::2], sources[1::2]):
        for map in maps:
            if start in range(map['src'], map['src'] + map['num']):
                mapped_start = start - (map['src'] - map['dst'])
                mapped_end = start + amount - (map['src'] - map['dst'])
                if mapped_end < map['dst'] + map['num']:
                    return mapped_start, mapped_end - mapped_start  # return a destination range
                else:  # given range is bigger than the found map's range
                    # return values for found range + values overflow
                    rest_amount = mapped_end - (map['dst'] + map['num'])
                    return mapped_start, amount - rest_amount, _calc_destination(maps, map['src'] + map['num'], rest_amount)
    # Any source numbers that aren't mapped correspond to the same destination number
    return start, amount  # destination range is same as source range


# def _map_src_to_dst(src, dst, start, amount):
def _map_src_to_dst(src, dst, *sources):
    """rewrote to work with ranges instead of individual values"""
    current_mapping = None
    for mapping in mappings:
        if mapping['src'] == src.strip():  # found the mapping with the correct src
            current_mapping = mapping
            break
    if current_mapping['dst'] == dst.strip():  # the mapping also has the correct dst
        return _calc_destination(current_mapping['maps'], *sources)
    else:  # get the next level mapping
        return _map_src_to_dst(current_mapping['dst'], dst, *_calc_destination(current_mapping['maps'], *sources))


def find_lowest_location(seed_line):
    """rewrote to work with ranges instead of each individual values"""
    lowest_location = None
    seed_numbers = seed_line.split()[1:]  # skip first element ('seeds:')

    for start, amount in zip(seed_numbers[0::2], seed_numbers[1::2]):
        print(start, amount)
        locations = _map_src_to_dst('seed', 'location', int(start), int(amount))
        print(locations)

    return lowest_location


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    create_mappings(data_lines)
    # pprint(mappings)

    seed = 79, 14
    print('seed =', seed)
    print('soil =', _map_src_to_dst('seed', 'soil', *seed))  # should be (81, 14)
    print('fertilizer =', _map_src_to_dst('seed', 'fertilizer', *seed))  # should be (81, 14)
    print('water =', _map_src_to_dst('seed', 'water', *seed))  # should be (81, 14)
    print('light =', _map_src_to_dst('seed', 'light', *seed))  # should be (74, 14)
    print('temperature =', _map_src_to_dst('seed', 'temperature', *seed))  # should be (74, 3, 55, 11)
    # print('humidity =', _map_src_to_dst('seed', 'humidity', *seed))  # should be 78
    # print('location =', _map_src_to_dst('seed', 'location', *seed))  # should be 82

    # lowest_location = find_lowest_location(data_lines[0])

    # print(f'End result: {lowest_location}')

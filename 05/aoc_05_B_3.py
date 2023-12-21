# aoc_05_B_3.py - Day 5: If You Give A Seed A Fertilizer - part 2
# build translation maps from text file and use them to find locations
# instead of just a list of seed numbers, the seed line must now be considered containing pairs of numbers,
# the first in the pair being the start number, the second one the number of seeds
# the naive approach from aoc_05_B_1.py (calculating each and every number) takes way too long,
# this program will find the target mapping that yields the smallest output (range) and
# work its way back to find the (range(s) of) seed(s) to result in that output (range)
# https://adventofcode.com/2023/day/5


from aoc_05_A_3 import (
    DATA_PATH,
    load_data,
    test_data,
    mappings,
    create_mappings,  # just stores range start and length values
)

from pprint import pprint
import time
from tools import convertSeconds

MAX_MAP = 100_000_000
# MAX_MAP = 100


seed_ranges = []


def _fill_mapping(mapping):
    # fill from zero to the lowest source value
    for i in range(min(mapping.keys())):
        mapping.update({i: i})
    # fill from the highest source value to MAX_MAP
    for i in range(max(mapping.keys()) + 1, MAX_MAP):
        mapping.update({i: i})


def generate_mappings(data_lines):
    """fills all mappings explicitely - only for visualisation with small test data set"""
    global mappings
    current_mapping = {}
    for line in data_lines:
        if line and line.lower().startswith('seeds'):  # don't need this to create maps
            continue
        elif line.strip() and line.strip().lower().endswith('map:'):  # found the first line of a new map
            src, _, dst = line.split()[0].split('-')
            current_mapping['src'] = src
            current_mapping['dst'] = dst
            current_mapping['maps'] = {}
        elif line.strip() and line.strip()[0].isdigit():  # found a data line for the current map
            dst, src, num = line.split()
            src_range = range(int(src), int(src) + int(num))
            dst_range = range(int(dst), int(dst) + int(num))
            current_mapping['maps'].update(zip(src_range, dst_range))  # add mapping to current_map's map
        elif not line.strip():  # empty line indicates end of current mapping
            if current_mapping:  # avoid adding empty mappings in case of multiple empty lines
                _fill_mapping(current_mapping['maps'])
                mappings.append(current_mapping)
                current_mapping = {}  # reset for reuse
    # add the last mapping, if any
    if current_mapping:  # avoid adding empty mappings just in case
        _fill_mapping(current_mapping['maps'])
        mappings.append(current_mapping)


def create_seed_ranges(seed_line):
    """extract seed ranges from the first line of the input
    avoids having to do this every time a seed value is checked"""
    global seed_ranges

    seed_numbers = seed_line.split()[1:]  # skip first element ('seeds:')

    for start, amount in zip(seed_numbers[0::2], seed_numbers[1::2]):
        seed_ranges.append(range(int(start), int(start) + int(amount)))


def _calc_source(maps, val):
    for map in maps:
        if val in range(map['dst'], map['dst'] + map['num']):
            return val + (map['src'] - map['dst'])
    # 'Any source numbers that aren't mapped correspond to the same destination number'
    # this also means that if a destination value is not found, it is possible there is no source value that maps to it
    # let's assume for now that all ranges are carefully chosen to not have that problem
    return val


def reverse_map(src, dst, val):
    if src not in [mapping['src'] for mapping in mappings]:
        raise KeyError(f'source "{src}" not in mappings')
    if dst not in [mapping['dst'] for mapping in mappings]:
        raise KeyError(f'destination "{dst}" not in mappings')

    current_mapping = None
    for mapping in mappings:
        if mapping['dst'] == dst.strip():  # found the mapping with the correct dst
            current_mapping = mapping
            break
    # we don't check if current_mapping contains anything,
    # because we already confirmed src (and dst) are in the mappings
    if current_mapping and current_mapping['src'] == src.strip():  # the mapping also has the correct src
        return _calc_source(current_mapping['maps'], val)  # end of the line, return the mapped value
    else:  # not quite there yet, so get the next (previous) level mapping
        return reverse_map(src, current_mapping['src'], _calc_source(current_mapping['maps'], val))


def verify_seed(seed):
    for seed_range in seed_ranges:
        if seed in seed_range:
            return True
    return False


tests = [
    # ('not_a_src', 'not_a_dst', 0),  # should raise KeyError
    # ('soil', 'not_a_dst', 0),  # should raise KeyError
    ('humidity', 'location', 60),  # with explicit mapping - should be 56
    ('humidity', 'location', 55),  # without explicit mapping - should be 55
    ('humidity', 'location', 56),  # should be 93
    ('temperature', 'location', 60),  # should be 55
    ('temperature', 'location', 55),  # should be 54
    ('temperature', 'location', 56),  # should be 93
    ('light', 'location', 60),  # should be 87
    ('light', 'location', 55),  # should be 86
    ('light', 'location', 56),  # should be 57
    ('water', 'location', 60),  # should be 94
    ('water', 'location', 55),  # should be 93
    ('water', 'location', 56),  # should be 64
    ('fertilizer', 'location', 60),  # should be 94
    ('fertilizer', 'location', 55),  # should be 93
    ('fertilizer', 'location', 56),  # should be 64
    ('soil', 'location', 60),  # should be 94
    ('soil', 'location', 55),  # should be 93
    ('soil', 'location', 56),  # should be 64
    ('seed', 'location', 60),  # should be 92
    ('seed', 'location', 55),  # should be 91
    ('seed', 'location', 56),  # should be 62
    ('seed', 'location', 46),  # from the example - should be 82
]

if __name__ == '__main__':
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    # generate_mappings(data_lines)
    # pprint(mappings)

    # look at the explicit mapping when the humidity-to-location map 56 93 4 is not present
    # for visualisation with small test data set
    # generate_mappings(data_lines[:-1])
    # pprint(mappings)

    # test what happens when the humidity-to-location map 56 93 4 is not present
    # create_mappings(data_lines[:-1])
    # pprint(mappings)

    create_mappings(data_lines)
    # pprint(mappings)

    create_seed_ranges(data_lines[0])
    # pprint(seed_ranges)

    # determine largest value in seed ranges
    largest_seed_number = max(
        seed_range.stop for seed_range in seed_ranges
    )
    print(f'the largest seed number is {largest_seed_number:,}')

    # generate csv from mappings for easier tracking of reverse mappings
    # with open('mappings.csv', 'w') as f:
    #     line = ''
    #     # generate header line
    #     for mapping in mappings:
    #         line += mapping['src'] + ';' + mapping['dst'] + ';'
    #     f.write(line[:-1] + '\n')
    #
    #     # generate data lines
    #     for i in range(MAX_MAP):
    #         line = ''
    #         for mapping in mappings:  # generate header line
    #             line += str(i) + ';' + str(mapping['map'][i]) + ';'
    #         f.write(line[:-1] + '\n')

    # test reverse_map with some edge cases
    # for src, dst, val in tests:
    #     print(f'{src} {reverse_map(src, dst, val)} maps to location {val}')

    # test verify_seed
    # for seed in 54, 55, 67, 68:  # 0, 1, 1, 0
    #     print(f'seed {seed} is {"" if verify_seed(seed) else "not "}one of the seeds to be planted')

    # for seed in range(MAX_MAP):
    #     print(f'seed {seed} is {"" if verify_seed(seed) else "not "}one of the seeds to be planted')

    # loop through all 'available' locations and reverse find the corresponding seed
    # if the seed is in one of the seed ranges we found the lowest possible location
    # because we started with the lowest possible value and only increment if a
    # corresponding seed was not found
    start_time = time.time()  # make note of start time (to calculate running time at end)

    for location in range(MAX_MAP):
        seed = reverse_map('seed', 'location', location)
        if verify_seed(seed):
            print(f'seed {seed:,} maps to location {location:,} and is one of the seeds to be planted')
            break
    else:
        print(f'couldn\'t find any locations for the first {MAX_MAP:,} seeds')

    print(f'finished in {convertSeconds(time.time() - start_time)}')

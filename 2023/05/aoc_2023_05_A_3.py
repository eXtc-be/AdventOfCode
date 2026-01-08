# aoc_2023_05_A_3.py - Day 5: If You Give A Seed A Fertilizer - part 1
# What is the lowest location number that corresponds to any of the initial seed numbers?
# https://adventofcode.com/2023/day/5
# not much of a difference with aoc_2023_05_A_2.py, except for maps being renamed to mappings
# and being a list instead of a dict
# I actually had to rewrite this from scratch because I forgot to copy it to my thumb drive :)


from aoc_2023_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def create_mappings(data_lines: list[str]) -> None:  # changes global variable directly
    global mappings

    current_mapping = {}
    for line in data_lines[2:]:  # skip first 2 lines (seed numbers + empty line)
        if line.strip() and line.strip().lower().endswith('map:'):  # found the first line of a new map
            src, _, dst = line.split()[0].split('-')
            current_mapping['src'] = src.strip()
            current_mapping['dst'] = dst.strip()
            current_mapping['maps'] = []  # will hold all maps for this mapping
        if line.strip() and line.strip()[0].isdigit():  # found a mapping line
            dst, src, num = line.split()
            current_mapping['maps'].append({'src': int(src), 'dst': int(dst), 'num': int(num)})
        if not line.strip():  # empty line indicates end of current mapping
            if current_mapping:  # avoid adding empty mappings in case of multiple empty lines
                mappings.append(current_mapping)
                current_mapping = {}  # reset for reuse
    # add the last mapping, if any
    if current_mapping:  # avoid adding empty mappings just in case
        mappings.append(current_mapping)


def _calc_destination(maps: dict, value: int) -> int:
    for map in maps:
        if value in range(map['src'], map['src'] + map['num']):
            return value + (map['dst'] - map['src'])
    # Any source numbers that aren't mapped correspond to the same destination number
    return value


def _map_src_to_dst(src: str, dst: str, val: int) -> int:
    current_mapping = None
    for mapping in mappings:
        if mapping['src'] == src.strip():  # found the mapping with the correct src
            current_mapping = mapping
            break

    if current_mapping['dst'] == dst.strip():  # the mapping also has the correct dst
        return _calc_destination(current_mapping['maps'], val)
    else:  # get the next level mapping
        return _map_src_to_dst(current_mapping['dst'], dst, _calc_destination(current_mapping['maps'], val))


def find_locations(seed_line: str) -> list[int]:
    locations = []

    for seed in seed_line.split()[1:]:  # skip first element ('seeds:')
        locations.append(_map_src_to_dst('seed', 'location', int(seed)))

    return locations


mappings = []


@time_it
def main(data_lines: list[str]) -> None:
    create_mappings(data_lines)
    # pprint(mappings)

    locations = find_locations(data_lines[0])
    # print(locations)

    print(f'End result: {min(locations)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 35
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 175622908
    #   Finished 'main' in 1 millisecond

    # create_mappings(test_data)
    # seed = 79
    # print('seed =', seed)
    # print('soil =', _map_src_to_dst('seed', 'soil', seed))  # should be 81
    # print('fertilizer =', _map_src_to_dst('seed', 'fertilizer', seed))  # should be 81
    # print('water =', _map_src_to_dst('seed', 'water', seed))  # should be 81
    # print('light =', _map_src_to_dst('seed', 'light', seed))  # should be 74
    # print('temperature =', _map_src_to_dst('seed', 'temperature', seed))  # should be 78
    # print('humidity =', _map_src_to_dst('seed', 'humidity', seed))  # should be 78
    # print('location =', _map_src_to_dst('seed', 'location', seed))  # should be 82


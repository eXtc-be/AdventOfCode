# aoc_2023_05_A_1.py - Day 5: If You Give A Seed A Fertilizer - part 1
# What is the lowest location number that corresponds to any of the initial seed numbers?
# https://adventofcode.com/2023/day/5
# numbers in the input file are too big to create maps explicitly, so we just record source, destination and amount
# when doing the actual mapping we now can't use 'if val in map' anymore,
# nor can we do map['map'][value] to get the new value;
# instead we need to check if value falls between source and source + amount, and calculate the new value


from aoc_2023_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def generate_maps(data_lines: list[str]) -> None:  # changes global variable directly
    global maps

    current_map = ''
    for line in data_lines:
        if line and line.lower().startswith('seeds'):  # don't need this to create maps
            continue
        elif line and line.lower().endswith('map:'):  # found the start of a new map
            current_map = line.split()[0]
            maps[current_map] = {}
            src, _, dst = current_map.split('-')
            maps[current_map]['src'] = src
            maps[current_map]['dst'] = dst
            maps[current_map]['map'] = []
        elif line and line[0].isdigit():  # found a data line for the current map
            dst, src, num = line.split()
            maps[current_map]['map'].append({'src': int(src), 'dst': int(dst), 'num': int(num)})
        else:
            continue


def _calc_destination(mappings: dict, value: int) -> int:
    for map in mappings:
        if value in range(map['src'], map['src'] + map['num']):
            return value + (map['dst'] - map['src'])
    # Any source numbers that aren't mapped correspond to the same destination number
    return value


def _map_x_to_y(src: str, dst: str, value: int) -> int:
    if src not in [map['src'] for map in maps.values()]:
        raise KeyError(f'source "{src}" not in maps')
    if dst not in [map['dst'] for map in maps.values()]:
        raise KeyError(f'destination "{dst}" not in maps')

    # find the map with the source we need
    mappings = None
    for _, mappings in maps.items():
        if mappings['src'] == src:
            break  # no need to look any further

    # no need to check if current_map has a value because we already confirmed src is in map
    # use the map we just found to map from src to some destination
    retval = _calc_destination(mappings['map'], value)

    if mappings['dst'] == dst:  # we found the map with the destination we need, so we can return the mapped value
        return retval
    else:  # the destination we need is not the one we found, so try to find it with the found destination as source
        return _map_x_to_y(mappings['dst'], dst, retval)


def find_locations(seed_line: str) -> list[int]:
    seeds = seed_line.split()[1:]
    
    locations = []
    for seed in seeds:
        locations.append(_map_x_to_y('seed', 'location', int(seed)))
    return locations


maps = {}


@time_it
def main(data_lines: list[str]) -> None:
    generate_maps(data_lines)
    # pprint(maps)

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

    # generate_maps(test_data)
    # test = _map_x_to_y('seed', 'soil', 79)
    # print(f'79 -> {test}')
    # test = _map_x_to_y('seed', 'fertilizer', 14)
    # print(f'14 -> {test}')
    # test = _map_x_to_y('seed', 'water', 55)
    # print(f'55 -> {test}')
    # test = _map_x_to_y('seed', 'location', 13)
    # print(f'13 -> {test}')


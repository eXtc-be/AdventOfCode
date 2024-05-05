# aoc_2023_05_A_1.py - Day 5: If You Give A Seed A Fertilizer - part 1
# What is the lowest location number that corresponds to any of the initial seed numbers?
# https://adventofcode.com/2023/day/5
# this version creates the maps explicitly: {a: x, b: y, etc.}


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_05'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


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
            maps[current_map]['map'] = {}
        elif line and line[0].isdigit():  # found a data line for the current map
            dst, src, num = line.split()
            src_range = range(int(src), int(src) + int(num))
            dst_range = range(int(dst), int(dst) + int(num))
            maps[current_map]['map'].update(zip(src_range, dst_range))  # add mapping to current_map's map
        else:
            continue


def _map_x_to_y(src: str, dst: str, value: int) -> int:
    if src not in [map['src'] for map in maps.values()]:
        raise KeyError(f'source "{src}" not in maps')
    if dst not in [map['dst'] for map in maps.values()]:
        raise KeyError(f'destination "{dst}" not in maps')

    # find the map with the source we need
    map = None
    for _, map in maps.items():
        if map['src'] == src:
            break  # no need to look any further

    # no need to check if current_map has a value because we already confirmed src is in map
    # use the map we just found to map from src to some destination
    if value in map['map']:
        retval = map['map'][value]
    else:
        # Any source numbers that aren't mapped correspond to the same destination number
        retval = value

    if map['dst'] == dst:  # we found the map with the destination we need, so we can return the mapped value
        return retval
    else:  # the destination we need is not the one we found, so try to find it with the found destination as source
        return _map_x_to_y(map['dst'], dst, retval)


def find_locations(seed_line: str) -> list[int]:
    seeds = seed_line.split()[1:]

    locations = []
    for seed in seeds:
        locations.append(_map_x_to_y('seed', 'location', int(seed)))
    return locations


test_data = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''.strip().splitlines()


maps = {}


@time_it
def main(data_lines: list[str]) -> None:
    generate_maps(data_lines)
    # pprint(maps)

    locations = find_locations(data_lines[0])
    # print(locations)

    print(f'End result: {min(locations)}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 35
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: ???
    #   Didn't finish 'main' (takes too long)

    # generate_maps(test_data)
    # test = _map_x_to_y('seed', 'soil', 79)
    # print(f'79 -> {test}')
    # test = _map_x_to_y('seed', 'fertilizer', 14)
    # print(f'14 -> {test}')
    # test = _map_x_to_y('seed', 'water', 55)
    # print(f'55 -> {test}')
    # test = _map_x_to_y('seed', 'location', 13)
    # print(f'13 -> {test}')


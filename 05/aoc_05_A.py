# aoc_05_A.py - Day 5: If You Give A Seed A Fertilizer - part 1
# create mappings from a text file and use them to map seed numbers to locations
# https://adventofcode.com/2023/day/5


from pprint import pprint


data_path = './input'


mappings = []


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def create_maps(data_lines):
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


def _calc_destination(maps, val):
    for map in maps:
        if val in range(map['src'], map['src'] + map['num']):
            return val + (map['dst'] - map['src'])
    # Any source numbers that aren't mapped correspond to the same destination number
    return val


def _map_src_to_dst(src, dst, val):
    current_mapping = None
    for mapping in mappings:
        if mapping['src'] == src.strip():  # found the mapping with the correct src
            current_mapping = mapping
            break
    if current_mapping['dst'] == dst.strip():  # the mapping also has the correct dst
        return _calc_destination(current_mapping['maps'], val)
    else:  # get the next level mapping
        return _map_src_to_dst(current_mapping['dst'], dst, _calc_destination(current_mapping['maps'], val))


def find_locations(seed_line):
    locations = []

    for seed in seed_line.split()[1:]:  # skip first element ('seeds:')
        locations.append(_map_src_to_dst('seed', 'location', int(seed)))

    return locations


test_data = """seeds: 79 14 55 13

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
""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(data_path)
    # data_lines = test_data
    # print(data_lines)

    create_maps(data_lines)
    # pprint(mappings)

    # seed = 79
    # print('seed =', seed)
    # print('soil =', _map_src_to_dst('seed', 'soil', 79))  # should be 81
    # print('fertilizer =', _map_src_to_dst('seed', 'fertilizer', 79))  # should be 81
    # print('water =', _map_src_to_dst('seed', 'water', 79))  # should be 81
    # print('light =', _map_src_to_dst('seed', 'light', 79))  # should be 74
    # print('temperature =', _map_src_to_dst('seed', 'temperature', 79))  # should be 78
    # print('humidity =', _map_src_to_dst('seed', 'humidity', 79))  # should be 78
    # print('location =', _map_src_to_dst('seed', 'location', 79))  # should be 82

    locations = find_locations(data_lines[0])  # first line contains seed numbers
    print(locations)

    print(f'End result: {min(locations)}')

# aoc_2015_09_A_1.py - Day 9: All in a Single Night - part 1
# What is the distance of the shortest route?
# https://adventofcode.com/2015/day/9


from tools import time_it

from itertools import permutations

from pprint import pprint


DATA_PATH = './input_2015_09'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_map(data_lines: list[str]) -> dict[str, dict[str, int]]:
    map = {}

    for line in data_lines:
        src, _, dst, _,  dist = line.split()
        if src not in map:
            map[src] = {}
        map[src][dst] = int(dist)
        if dst not in map:
            map[dst] = {}
        map[dst][src] = int(dist)

    return map


def _get_distance(locations: tuple[str, ...], map: dict[str, dict[str, int]]) -> tuple[tuple[str, ...], int]:
    distance = 0
    for src, dst in zip(locations, locations[1:]):
        distance += map[src][dst]

    return locations, distance


def get_distances(map: dict[str, dict[str, int]]) -> list[tuple[tuple[str, ...], int]]:
    return [_get_distance(combo, map) for combo in permutations(map.keys(), r=len(map.keys()))]


test_data = '''
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    map = get_map(data_lines)
    # pprint(map)

    distances = get_distances(map)
    # pprint(distances)

    shortest = sorted(distances, key=lambda d: d[1])[0]
    print(f'End result: {" -> ".join(shortest[0])} = {shortest[1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: London -> Dublin -> Belfast = 605
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: Tambi -> Arbre -> Snowdin -> AlphaCentauri -> Tristram -> Straylight -> Faerun -> Norrath = 251
    #   Finished 'main' in 90 milliseconds

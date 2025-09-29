# aoc_2024_10_A_1.py - Day 10: Hoof It - part 1
# What is the sum of the scores of all trailheads on your topographic map?
# https://adventofcode.com/2024/day/10


from tools import time_it

# other imports

from pprint import pprint
from dataclasses import dataclass, field
from enum import Enum


DATA_PATH = './input_2024_10'

# other constants


@dataclass
class Coord:
    x: int = 0
    y: int = 0

    # def distance(self, other: 'Coord' = None) -> int:
    #     other = Coord(0, 0) if other is None else other
    #     return abs(self.x - other.x) + abs(self.y - other.y)
    #
    def __add__(self, other: 'Coord'):
        return Coord(self.x + other.x, self.y + other.y)

    # def __sub__(self, other: 'Coord'):
    #     return Coord(self.x - other.x, self.y - other.y)
    #
    # def __str__(self):
    #     return f'({self.x}, {self.y})'
    #
    def __hash__(self):
        return hash((self.x, self.y))


class Heading(Enum):
    north = Coord(0, -1)
    east = Coord(1, 0)
    south = Coord(0, 1)
    west = Coord(-1, 0)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def create_map(data_lines: list[str]) -> list[list[int]]:
    return [[int(el) for el in line] for line in data_lines]


def extract_trailheads(topo_map: list[list[int]]) -> list[Coord]:
    trailheads = []

    for y, line in enumerate(topo_map):
        for x, val in enumerate(line):
            if val == 0:
                trailheads.append(Coord(x, y))

    return trailheads


def find_trails(topo_map: list[list[int]], start: Coord) -> list[list[Coord]]:
    if topo_map[start.y][start.x] == 9:
        return [[start]]

    trails = []

    for heading in Heading:
        next_pos = start + heading.value
        if 0 <= next_pos.x < len(topo_map[0]) and 0 <= next_pos.y < len(topo_map):  # check whether next_pos is within the map
            if topo_map[next_pos.y][next_pos.x] == topo_map[start.y][start.x] + 1:  # check whether elevation of next_pos is one more than start
                for trail in find_trails(topo_map, next_pos):  # loop through all trails starting from next_pos
                    if topo_map[trail[-1].y][trail[-1].x] == 9:  # check whether a given trail ends at elevation 9
                        trails.append([start] + trail)

    return trails


test_data = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    topo_map = create_map(data_lines)
    # pprint(topo_map)

    trailheads = extract_trailheads(topo_map)
    # pprint(trailheads)

    result = 0
    for trailhead in trailheads:
        trails = find_trails(topo_map, trailhead)
        # pprint(trails)
        unique_endpoints = set(trail[-1] for trail in trails)
        # print(len(unique_endpoints))
        result += len(unique_endpoints)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 36
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 786
    #   Finished 'main' in 34 milliseconds

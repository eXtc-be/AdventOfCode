# aoc_2018_22_B_1.py - Day 22: Mode Maze - part 2
# What is the fewest number of minutes you can take to reach the target?
# https://adventofcode.com/2018/day/22
# this version uses standard A*, lots of room for improvement
# (not all lists are necessary, and when they get big, they tend to slow the program way down)


from aoc_2018_22_A_1 import (
    DATA_PATH,
    Y_0,
    X_0,
    MODULO,
    TYPES,
    load_data,
    get_inputs,
    test_data,
)

from tools import time_it

from dataclasses import dataclass
from enum import Enum

from pprint import pprint


DEBUG = '{coord} [{region:>6}] w/ {gear:>8} @ t={total:4}'


class Gear(Enum):
    torch = 0
    climbing = 1
    neither = 2


GEAR = {
    0: Gear.torch,
    1: Gear.climbing,
    2: Gear.neither,
}


class Region(Enum):
    rocky = 0
    wet = 1
    narrow = 2


REGION = {
    0: Region.rocky,
    1: Region.wet,
    2: Region.narrow,
}


REGION_GEAR = {
    Region.rocky: [Gear.torch, Gear.climbing],
    Region.wet: [Gear.climbing, Gear.neither],
    Region.narrow: [Gear.torch, Gear.neither],
}


@dataclass
class Coord:
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'({self.x:4},{self.y:4})'

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Grid:
    target: Coord
    depth: int

    def __post_init__(self):
        # self.grid = [[-1 for c in range(self.target.x+1000)] for r in range(self.target.y+1000)]
        # self.auto_expand = False
        # self.grid = [[-1 for c in range(self.target.x*5)] for r in range(self.target.y*5)]
        # self.auto_expand = False
        self.grid = [[-1 for c in range(self.target.x+1)] for r in range(self.target.y+1)]
        self.auto_expand = True

        self.calc_levels()

    def __getitem__(self, coord: Coord) -> int:
        if self.auto_expand:
            if coord.y >= len(self.grid):
                self.expand(0, 1)  # expand grid vertically
            if coord.x >= len(self.grid[0]):
                self.expand(1, 0)  # expand grid vertically
        return self.grid[coord.y][coord.x]

    def __setitem__(self, coord: Coord, data: int):
        self.grid[coord.y][coord.x] = data

    def __str__(self) -> str:
        return '\n'.join(''.join(TYPES[self.region(c)] for c in row) for row in self.grid)

    def expand(self, width: int, height: int) -> None:
        for r in range(height):
            self.grid.append([-1 for c in range(len(self.grid[0]))])

        for c in range(width):
            for row in self.grid:
                row.append(-1)

        self.calc_levels()

    def _calc_index(self, coord: Coord) -> int:
        if coord == Coord(0, 0) or coord == self.target:
            return 0
        elif coord.y == 0:
            return coord.x * Y_0
        elif coord.x == 0:
            return coord.y * X_0
        else:
            return self[Coord(coord.x-1, coord.y)] * self[Coord(coord.x, coord.y-1)]

    def calc_levels(self) -> None:
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] < 0:
                    self[Coord(c, r)] = (self._calc_index(Coord(c, r)) + self.depth) % MODULO

    @staticmethod
    def region(level: int) -> int:
        return level % 3

    def _heuristic(self, n: Coord) -> int:
        # return self.target.distance(n) * 8
        # return self.target.distance(n)
        return 0

    def _get_neighbors(self, v: Coord, current_gear: Gear) -> list[tuple[Coord, Gear, int]]:
        neighbours = []

        for gear in Gear:  # try swapping gear at current position
            if gear in REGION_GEAR[REGION[self.region(self[v])]]:  # gear must be usable in current region
                neighbours.append((v, gear, 7))  # append 'neighbour' with weight 7

        for direction in (Coord(0, -1), Coord(0, 1), Coord(-1, 0), Coord(1, 0)):
            if (v+direction).x >= 0 and (v+direction).y >= 0:  # can't go to regions with negative x or y
                if current_gear in REGION_GEAR[REGION[self.region(self[v+direction])]]:
                    neighbours.append((v + direction, current_gear, 1))

        return neighbours

    def find_path(self) -> list[tuple[Coord, Gear]] | None:
        open_list = {(Coord(0, 0), Gear.torch)}
        closed_list = set()
        distances = {(Coord(0, 0), Gear.torch): 0}
        parents = {(Coord(0, 0), Gear.torch): (Coord(0, 0), Gear.torch)}

        while open_list:
            n = None

            for v in open_list:
                # if n is None or distances[v] + self._heuristic(v[0]) < distances[n] + self._heuristic(n[0]):
                if n is None or distances[v] < distances[n]:
                    n = v

            if n is None:
                return None

            if n == (self.target, Gear.torch):
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append((Coord(0, 0), Gear.torch))  # re-add start

                path.reverse()

                return path

            for (m, g, weight) in self._get_neighbors(*n):
                if (m, g) not in open_list and (m, g) not in closed_list:
                    open_list.add((m, g))
                    parents[(m, g)] = n
                    distances[(m, g)] = distances[n] + weight
                else:
                    if distances[(m, g)] > distances[n] + weight:
                        distances[(m, g)] = distances[n] + weight
                        parents[(m, g)] = n

                        if (m, g) in closed_list:
                            closed_list.remove((m, g))
                            open_list.add((m, g))

            open_list.remove(n)
            closed_list.add(n)
            if len(closed_list) % 1000 == 0:
                print(len(closed_list), len(self.grid), len(self.grid[0]))

        return None


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    depth, target = get_inputs(data_lines)

    grid = Grid(Coord(*target), depth)

    # pprint(grid.grid)
    # print(grid)

    path = grid.find_path()
    # print(path)

    # my_map = [[TYPES[Grid.region(c)] for c in row] for row in grid.grid]
    # # pprint(map)
    # for coord, gear in path:
    #     my_map[coord.y][coord.x] = 'o'
    # my_map[0][0] = 'M'
    # my_map[target[1]][target[0]] = 'T'
    # print('\n'.join([''.join([c for c in row]) for row in my_map]))

    total = 0
    gear = path[0][1]
    for i, (c, g) in enumerate(path):
        if g == gear:
            total += 1 if i > 0 else 0
        else:
            total += 7
            gear = g

        # print(DEBUG.format(
        #     coord=c,
        #     region=REGION[Grid.region(grid[c])].name,
        #     gear=g.name,
        #     total=total
        # ))

    print(f'End result: {total}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)
    # main(['depth: 510', 'target: 29,9'])

    # using test_data:
    #   End result: 45
    #   Finished 'main' in 31 milliseconds
    # using test_data 510; 29,9:
    #   End result: 65
    #   Finished 'main' in 176 milliseconds
    # using input data:
    #   End result: 944
    #   Finished 'main' in 25 minutes and 15 seconds

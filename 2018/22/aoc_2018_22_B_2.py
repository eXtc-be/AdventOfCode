# aoc_2018_22_B_1.py - Day 22: Mode Maze - part 2
# What is the fewest number of minutes you can take to reach the target?
# https://adventofcode.com/2018/day/22
# trying these optimizations:
#   - don't pre-calculate the cells in the grid, but only on first access (the cells still get pre-filled with None)
#   - use heapq
#   - eliminate as many lists/dicts as possible


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
import heapq

from pprint import pprint


DEBUG = '{coord} [{region:>6}] w/ {gear:>8} @ t={total:4}'


class Gear(Enum):
    torch = 0
    climbing = 1
    neither = 2

    def __lt__(self, other):
        return self.value < other.value


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

    def __lt__(self, other):
        return self.distance(Coord(0, 0)) < other.distance(Coord(0, 0))

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Grid:
    target: Coord
    depth: int

    def __post_init__(self):
        self.levels: list[list[int | None]] = [[None for c in range(self.target.x + 1)] for r in range(self.target.y + 1)]
        self.auto_expand = True

    def __getitem__(self, coord: Coord) -> int:
        if self.auto_expand:
            if coord.y >= len(self.levels):
                self.expand(0, 1)  # expand grid vertically
            if coord.x >= len(self.levels[0]):
                self.expand(1, 0)  # expand grid vertically

        if self.levels[coord.y][coord.x] is None:
            self.levels[coord.y][coord.x] = self._calc_level(coord)

        return self.levels[coord.y][coord.x]

    def __setitem__(self, coord: Coord, data: int):
        self.levels[coord.y][coord.x] = data

    def __str__(self) -> str:
        self.calc_levels()
        return '\n'.join(''.join(TYPES[self.region(c)] for c in row) for row in self.levels)

    def expand(self, width: int, height: int) -> None:
        for _ in range(height):
            self.levels.append([None for _ in range(len(self.levels[0]))])

        for row in self.levels:
            row.extend([None]*width)

    def _calc_index(self, coord: Coord) -> int:
        if coord == Coord(0, 0) or coord == self.target:
            return 0
        elif coord.y == 0:
            return coord.x * Y_0
        elif coord.x == 0:
            return coord.y * X_0
        else:
            return self[Coord(coord.x-1, coord.y)] * self[Coord(coord.x, coord.y-1)]

    def _calc_level(self, coord: Coord) -> int:
        return (self._calc_index(coord) + self.depth) % MODULO

    def calc_levels(self) -> None:
        for r in range(len(self.levels)):
            for c in range(len(self.levels[r])):
                if self.levels[r][c] is None:
                    self[Coord(c, r)] = (self._calc_index(Coord(c, r)) + self.depth) % MODULO

    @staticmethod
    def region(level: int) -> int:
        return level % 3

    def _get_neighbors(self, coord: Coord, current_gear: Gear) -> list[tuple[Coord, Gear, int]]:
        neighbours = []

        # current position with other gear
        for gear in Gear:
            if gear in REGION_GEAR[REGION[self.region(self[coord])]]:  # gear must be usable in current region
                neighbours.append((coord, gear, 7))  # append 'neighbour' with weight 7

        # all (reachable) neighbours with current gear
        for direction in (Coord(0, -1), Coord(0, 1), Coord(-1, 0), Coord(1, 0)):
            if (coord + direction).x >= 0 and (coord + direction).y >= 0:  # can't go to regions with negative x or y
                if current_gear in REGION_GEAR[REGION[self.region(self[coord + direction])]]:
                    neighbours.append((coord + direction, current_gear, 1))

        return neighbours

    def find_path(self) -> list[tuple[Coord, Gear]] | None:
        open_list = [(0, Coord(0, 0), Gear.torch)]  # cost, coord, gear
        costs = {(Coord(0, 0), Gear.torch): 0}  # coord, gear: cost
        # parents = {(Coord(0, 0), Gear.torch): (Coord(0, 0), Gear.torch)}

        while open_list:
            current_cost, current_coord, current_gear = heapq.heappop(open_list)

            if (current_coord, current_gear) == (self.target, Gear.torch):
                # path = []
                #
                # while parents[(current_coord, current_gear)] != (current_coord, current_gear):
                #     path.append((current_coord, current_gear))
                #     (current_coord, current_gear) = parents[(current_coord, current_gear)]
                #
                # path.append((Coord(0, 0), Gear.torch))  # re-add start
                #
                # path.reverse()
                #
                # return path

                return costs[(current_coord, current_gear)]

            for (coord, gear, cost) in self._get_neighbors(current_coord, current_gear):
                if (coord, gear) in costs and costs[(coord, gear)] <= current_cost + cost:
                    continue

                heapq.heappush(open_list, (current_cost + cost, coord, gear))
                costs[(coord, gear)] = current_cost + cost
                # parents[(coord, gear)] = (current_coord, current_gear)

                if len(costs) % 10000 == 0:
                    print(len(costs), len(self.levels), len(self.levels[0]))

        return None  # explicitly return None if no path was found


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    depth, target = get_inputs(data_lines)

    grid = Grid(Coord(*target), depth)

    # pprint(grid.grid)
    # print(grid)

    cost = grid.find_path()
    # path = grid.find_path()
    # print(path)

    # grid.calc_levels()  # make sure all levels are calculated
    # my_map = [[TYPES[Grid.region(c)] for c in row] for row in grid.levels]
    # # pprint(map)
    # for coord, gear in path:
    #     my_map[coord.y][coord.x] = 'o'
    # my_map[0][0] = 'M'
    # my_map[target[1]][target[0]] = 'T'
    # print('\n'.join([''.join([c for c in row]) for row in my_map]))

    # total = 0
    # gear = path[0][1]
    # for i, (c, g) in enumerate(path):
    #     if g == gear:
    #         total += 1 if i > 0 else 0
    #     else:
    #         total += 7
    #         gear = g
    #
    #     # print(DEBUG.format(
    #     #     coord=c,
    #     #     region=REGION[Grid.region(grid[c])].name,
    #     #     gear=g.name,
    #     #     total=total
    #     # ))

    print(f'End result: {cost}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)
    # main(['depth: 510', 'target: 29,9'])

    # using test_data:
    #   End result: 45
    #   Finished 'main' in 24 milliseconds
    # using test_data 510; 29,9:
    #   End result: 65
    #   Finished 'main' in 82 milliseconds
    # using input data:
    #   End result: 944
    #   Finished 'main' in 50 seconds with parents, 46 seconds without parents

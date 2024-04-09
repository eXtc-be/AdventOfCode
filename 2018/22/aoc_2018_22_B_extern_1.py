# aoc_2018_22_B_1.py - Day 22: Mode Maze - part 2
# What is the fewest number of minutes you can take to reach the target?
# https://adventofcode.com/2018/day/22
# based on a solution from reddit user u/mcpower_
# https://old.reddit.com/r/adventofcode/comments/a8i1cy/2018_day_22_solutions/ecax2bg/
# this version eliminates as much overhead as possible and is a lot faster than aoc_2018_22_B_1,
# although not as fast as the program it was based on (which does the real input in 6.3 seconds,
# compared to 54 seconds for this one) the reason is probably the added overhead of the classes


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
import heapq

from pprint import pprint


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

    def find_path(self) -> int | None:
        queue = [(0, Coord(0, 0), 1)]  # (minutes, coord, cannot)
        best = dict()  # (x, y, cannot) : minutes

        while queue:
            minutes, coord, cannot = heapq.heappop(queue)
            best_key = (coord, cannot)
            if best_key in best and best[best_key] <= minutes:
                continue
            best[best_key] = minutes
            if best_key == (self.target, 1):
                return minutes
            # for i in range(3):
            for i in range(3):
                if i != cannot and i != self.region(self[coord]):
                    heapq.heappush(queue, (minutes + 7, coord, i))

            # try going up down left right
            for direction in [Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1)]:
                new = coord + direction
                if new.x < 0:
                    continue
                if new.y < 0:
                    continue
                if self.region(self[new]) == cannot:
                    continue
                heapq.heappush(queue, (minutes + 1, new, cannot))

            if len(best) % 1000 == 0:
                print(len(best), len(self.grid), len(self.grid[0]))


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    depth, target = get_inputs(data_lines)

    grid = Grid(Coord(*target), depth)

    minutes = grid.find_path()

    print(f'End result: {minutes}')

    print(len(grid.grid), len(grid.grid[0]))


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)
    # main(['depth: 510', 'target: 29,9'])

    # using test_data:
    #   End result: 45
    #   Finished 'main' in 26 milliseconds
    # using test_data 510; 29,9:
    #   End result: 65
    #   Finished 'main' in 55 milliseconds
    # using input data:
    #   End result: 944
    #   Finished 'main' in 54 seconds

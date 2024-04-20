# aoc_2017_22_A_2.py - Day 22: Sporifica Virus - part 1
# After 10_000 bursts of activity, how many bursts cause a node to become infected?
# https://adventofcode.com/2017/day/22
# turns out keeping track of infected cells in a list of Points
# is actually slower than keeping the whole array in a dictionary:
#   went from 2 seconds to 15 milliseconds for 10000 rounds

from tools import time_it

from dataclasses import dataclass
from itertools import product
from collections import defaultdict

from pprint import pprint


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def distance(self, other: 'Point') -> int:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        return dx + max(0, (dy - dx) // 2)


DATA_PATH = './input_2017_22'

HEADINGS = {
    'N': {'L': 'W', 'R': 'E'},
    'E': {'L': 'N', 'R': 'S'},
    'S': {'L': 'E', 'R': 'W'},
    'W': {'L': 'S', 'R': 'N'},
}

DIRECTIONS = {
    'N': Point(0, 1),
    'E': Point(1, 0),
    'S': Point(0, -1),
    'W': Point(-1, 0),
}

INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'
CLEAN = '.'

STATES = {
    CLEAN: 0,
    INFECTED: 1,
    WEAKENED: 2,
    FLAGGED: 3,
}
STATES_INV = {v: k for k, v in STATES.items()}

ROUNDS = 10_000
ROUNDS_TEST = 70


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_grid(data_lines: list[str]) -> dict[Point, int]:
    grid = {}

    for x, y in product(range(-(len(data_lines) // 2), len(data_lines) // 2 + 1), repeat=2):
        r = len(data_lines) // 2 - y
        c = x + len(data_lines[0]) // 2
        grid[Point(x, y)] = STATES[data_lines[r][c]]

    return defaultdict(int, grid)


new_infections = 0


def do_step(grid: dict[Point, int], location: Point, heading: str) -> tuple[Point, str]:
    global new_infections
    turn = None

    if STATES_INV[grid[location]] == INFECTED:
        turn = 'R'
        grid[location] = STATES[CLEAN]
    elif STATES_INV[grid[location]] == CLEAN:
        turn = 'L'
        grid[location] = STATES[INFECTED]
        new_infections += 1

    new_heading = HEADINGS[heading][turn]
    new_location = location + DIRECTIONS[new_heading]

    return new_location, new_heading


def draw_grid(grid: dict[Point, int], loc: Point = None) -> None:
    min_x = min(p.x for p in list(grid.keys()) + [loc])
    min_y = min(p.y for p in list(grid.keys()) + [loc])
    max_x = max(p.x for p in list(grid.keys()) + [loc])
    max_y = max(p.y for p in list(grid.keys()) + [loc])

    for r in range(max_y, min_y - 1, -1):
        for c in range(min_x, max_x + 1):
            char = STATES_INV[grid[Point(c, r)]]
            if Point(c, r) == loc:
                print(f'[{char}]', end='')
            else:
                print(f' {char} ', end='')
        print()


test_data = '''
..#
#..
...
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS, verbose: bool = False) -> None:
    global new_infections

    grid = get_grid(data_lines)
    # print(grid)

    min_x = min(p.x for p in grid.keys())
    min_y = min(p.y for p in grid.keys())
    max_x = max(p.x for p in grid.keys())
    max_y = max(p.y for p in grid.keys())

    location = Point(min_x + (max_x - min_x) // 2, min_y + (max_y - min_y) // 2)
    heading = 'N'

    if verbose:
        print(0, location, heading)
        draw_grid(grid, location)
        print('-' * 100)

    for round in range(1, rounds + 1):
        location, heading = do_step(grid, location, heading)
        if verbose:
            print(round, location, heading)
            draw_grid(grid, location)
            print('-' * 100)

    print(f'End result: {new_infections}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, ROUNDS_TEST, True)
    # using test_data with 10000 rounds:
    #   End result: 5587
    #   Finished 'main' in 14 milliseconds
    # using input data:
    #   End result: 5280
    #   Finished 'main' in 15 milliseconds

    # # test get_grid
    # grid = get_grid(data_lines)
    # print(grid)

    # # test draw_grid
    # draw_grid(grid)
    # print('-' * 100)
    # grid[Point(-1, 1)] = 2
    # grid[Point(1, -1)] = 3
    # draw_grid(grid)
    # print('-' * 100)
    # draw_grid(grid, Point(0, 0))

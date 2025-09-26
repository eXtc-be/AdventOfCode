# aoc_2024_06_A_1.py - Day 6: Guard Gallivant - part 1
# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
# https://adventofcode.com/2024/day/6


from tools import time_it

# other imports

from pprint import pprint
from dataclasses import dataclass, field
from enum import Enum


DATA_PATH = './input_2024_06'

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


HEADING = {
    '^': Heading.north,
    '>': Heading.east,
    'v': Heading.south,
    '<': Heading.west,
}


TURNING = {  # changes the current heading into a new one when turning right
    Heading.north: Heading.east,
    Heading.east: Heading.south,
    Heading.south: Heading.west,
    Heading.west: Heading.north,
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def find_guard(layout: list[list[str]]) -> tuple[Coord, Heading]:
    for y, line in enumerate(layout):
        for x, char in enumerate(line):
            if char in '^>v<':
                return Coord(x, y), HEADING[char]

    return Coord(-1, -1), Heading.north


def patrol(layout: list[list[str]]) -> list[list[str]]:
    position, heading = find_guard(layout)

    grid = [[char for char in line] for line in layout]

    while True:
        grid[position.y][position.x] = 'X'  # mark visited
        next_pos = position + heading.value
        if 0 <= next_pos.x < len(layout[0]) and 0 <= next_pos.y < len(layout):
            if grid[next_pos.y][next_pos.x] in '.X':
                position = next_pos
            elif grid[next_pos.y][next_pos.x] == '#':
                heading = TURNING[heading]
                # position = position + heading.value
            else:
                raise ValueError(f'unexpected value at {next_pos}: {grid[next_pos.y][next_pos.x]}')
        else:
            break

    return grid


test_data = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    result = patrol([[char for char in line] for line in data_lines])

    print(f'End result: {sum(1 if c == "X" else 0 for line in result for c in line)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 41
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4580
    #   Finished 'main' in 6 milliseconds

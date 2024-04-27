# aoc_2019_11_A_1.py - Day 11: Space Police - part 1
# How many panels does your new emergency hull painting robot paint at least once?
# https://adventofcode.com/2019/day/11


import sys
sys.path.extend(['.', '..', '../..'])

from tools import time_it, clear
from intcode import Computer, State

from dataclasses import dataclass, field
from enum import Enum

from pprint import pprint


@dataclass
class Coord:
    x: int = 0
    y: int = 0

    def distance(self, other: 'Coord' = None) -> int:
        other = Coord(0, 0) if other is None else other
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other: 'Coord'):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord'):
        return Coord(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))


class Heading(Enum):
    north = Coord(0, 1)
    east = Coord(1, 0)
    south = Coord(0, -1)
    west = Coord(-1, 0)


HEADINGS = {
    Heading.north: '^',
    Heading.east: '>',
    Heading.south: 'v',
    Heading.west: '<',
}


class Turn(Enum):
    left = 0
    right = 1


TURN = {
    0: Turn.left,
    1: Turn.right,
}


TURNING = {  # changes the current heading into a new one when turning left or right
    Heading.north: {Turn.left: Heading.west, Turn.right: Heading.east},
    Heading.east: {Turn.left: Heading.north, Turn.right: Heading.south},
    Heading.south: {Turn.left: Heading.east, Turn.right: Heading.west},
    Heading.west: {Turn.left: Heading.south, Turn.right: Heading.north},
}


@dataclass
class Robot:
    computer: Computer
    position: Coord = field(default_factory=Coord)
    heading: Heading = Heading.north

    def __str__(self):
        return HEADINGS[self.heading]

    def move(self, turn: Turn):
        self.heading = TURNING[self.heading][turn]
        self.position += self.heading.value


class Color(Enum):
    black = 0
    white = 1

    def __str__(self):
        return COLORS[self]


COLOR = {
    0: Color.black,
    1: Color.white,
}


COLORS = {
    Color.black: '.',
    Color.white: '#',
}


@dataclass
class Hull:
    first: Color = Color.black
    panels: list[list[Color]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.panels = [[self.first]]
        self.origin = Coord(0, 0)

    @property
    def min_y(self) -> int:
        return -self.origin.y

    @property
    def max_y(self) -> int:
        return len(self.panels) - self.origin.y - 1

    @property
    def min_x(self) -> int:
        return -self.origin.x

    @property
    def max_x(self) -> int:
        return len(self.panels[0]) - self.origin.x - 1

    def expand(self, coord: Coord) -> None:
        if coord.y < self.min_y:  # grow vertically at start -> insert
            self.panels.insert(0, [Color.black for c in range(len(self.panels[0]))])
            self.origin.y += 1
        elif coord.y > self.max_y:  # grow vertically at end -> append
            self.panels.append([Color.black for c in range(len(self.panels[0]))])
        elif coord.x < self.min_x:  # grow horizontally at start -> insert
            for row in self.panels:
                row.insert(0, Color.black)
            self.origin.x += 1
        elif coord.x > self.max_x:  # grow horizontally at end -> append
            for row in self.panels:
                row.append(Color.black)

    def __getitem__(self, coord: Coord) -> Color:
        if not self.min_y <= coord.y <= self.max_y or not self.min_x <= coord.x <= self.max_x:
            self.expand(coord)

        return self.panels[coord.y + self.origin.y][coord.x + self.origin.x]

    def __setitem__(self, coord: Coord, color: Color):
        self.panels[coord.y + self.origin.y][coord.x + self.origin.x] = color

    def draw(self, robot: Robot = None) -> None:
        if robot:
            print(robot.position, robot.heading.name, self[robot.position].name)

        for r, row in reversed(list(enumerate(self.panels))):
            for c, panel in enumerate(row):
                if robot and robot.position == Coord(c, r) - self.origin:
                    print(str(robot), end='')
                else:
                    print(str(panel), end='')
            print()  # newline


DATA_PATH = './input_2019_11'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


@time_it
def main(data: str, verbose: bool = False, confirm: bool = False) -> None:
    painted = set()

    robot = Robot(Computer(list(map(int, data.split(','))), [], verbose))

    hull = Hull()
    if verbose:
        clear()
        hull.draw(robot)
        if confirm:
            input()

    while robot.computer.state != State.halted:
        robot.computer.run([hull[robot.position].value])
        hull[robot.position] = COLOR[robot.computer.outputs.pop(0)]
        painted.add(robot.position)
        robot.move(TURN[robot.computer.outputs.pop(0)])
        _ = hull[robot.position]  # access new position to force auto expanding the hull's panels array
        if verbose:
            clear()
            hull.draw(robot)
            if confirm:
                input()

    print(f'End result: {len(painted)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])

    # using input data:
    #   End result: 1934
    #   Finished 'main' in 1 second

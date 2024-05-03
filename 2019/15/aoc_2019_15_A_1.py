# aoc_2019_15_A_1.py - Day 15: Oxygen System - part 1
# What is the fewest number of movement commands required to move the repair droid
# from its starting position to the location of the oxygen system?
# https://adventofcode.com/2019/day/15
# if I had known part 2 would be about finding the shortest path to the location furthest away from the oxygen,
# I would probably have implemented part 1's search for the shortest path from the origin to the oxygen with
# Dijkstra, so I would have a list of all shortest paths. but I didn't know, so I did part 1 with A* instead.


import sys, os
sys.path.extend(['.', '..', '../..'])

from tools import time_it, clear
from intcode import Computer, State

from dataclasses import dataclass, field
from enum import Enum, auto
from sys import maxsize

from pprint import pprint


DATA_PATH = './input_2019_15'

MAZE_PATH = './maze.txt'


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

    def __lt__(self, other: 'Coord') -> bool:
        return abs(self.x) + abs(self.y) < abs(other.x) + abs(other.y)


class Heading(Enum):
    north = 1
    south = 2
    west = 3
    east = 4

    @property
    def opposite(self):
        if self == Heading.north:
            return Heading.south
        elif self == Heading.south:
            return Heading.north
        elif self == Heading.east:
            return Heading.west
        elif self == Heading.west:
            return Heading.east


HEADING = {
    Heading.north: Coord(0, -1),
    Heading.south: Coord(0, 1),
    Heading.west: Coord(-1, 0),
    Heading.east: Coord(1, 0),
}


HEADINGS = {
    Heading.north: '^',
    Heading.east: '>',
    Heading.south: 'v',
    Heading.west: '<',
}


class Type(Enum):
    unknown = auto()
    origin = auto()
    empty = auto()
    wall = auto()
    oxygen = auto()

    def __str__(self):
        return TYPES[self]


TYPE = {
    0: Type.wall,
    1: Type.empty,
    2: Type.oxygen,
}


TYPES = {
    Type.unknown: '?',
    Type.origin: 'O',
    Type.empty: '.',
    Type.wall: '#',
    Type.oxygen: 'X',
}


TYPING = {
    '?': Type.unknown,
    'O': Type.origin,
    '.': Type.empty,
    '#': Type.wall,
    'X': Type.oxygen,
}


class Turn(Enum):
    left = 0
    right = 1

    @property
    def opposite(self):
        if self == Turn.right:
            return Turn.left
        else:
            return Turn.right


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

    def __post_init__(self):
        self._last_turn = Turn.left

    def __str__(self):
        return HEADINGS[self.heading]

    def turn(self, turn: Turn = None):
        turn = self._last_turn.opposite if turn is None else turn
        self.heading = TURNING[self.heading][turn]
        self._last_turn = turn

    def move(self, heading: Heading = None) -> None:
        heading = self.heading if heading is None else heading
        self.position += HEADING[heading]


@dataclass
class Grid:
    grid: list[list[Type]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.grid:
            self.grid = [[Type.unknown]]

        self.origin = Coord(0, 0)
        self.oxygen = None

    @property
    def min_y(self) -> int:
        return -self.origin.y

    @property
    def max_y(self) -> int:
        return len(self.grid) - self.origin.y - 1

    @property
    def min_x(self) -> int:
        return -self.origin.x

    @property
    def max_x(self) -> int:
        return len(self.grid[0]) - self.origin.x - 1

    def expand(self, coord: Coord) -> None:
        if coord.y < self.min_y:  # grow vertically at start -> insert
            self.grid.insert(0, [Type.unknown for c in range(len(self.grid[0]))])
            self.origin.y += 1
        elif coord.y > self.max_y:  # grow vertically at end -> append
            self.grid.append([Type.unknown for c in range(len(self.grid[0]))])
        elif coord.x < self.min_x:  # grow horizontally at start -> insert
            for row in self.grid:
                row.insert(0, Type.unknown)
            self.origin.x += 1
        elif coord.x > self.max_x:  # grow horizontally at end -> append
            for row in self.grid:
                row.append(Type.unknown)

    def __getitem__(self, coord: Coord) -> Type:
        if not self.min_y <= coord.y <= self.max_y or not self.min_x <= coord.x <= self.max_x:
            self.expand(coord)

        return self.grid[coord.y + self.origin.y][coord.x + self.origin.x]

    def __setitem__(self, coord: Coord, value: Type):
        if not self.min_y <= coord.y <= self.max_y or not self.min_x <= coord.x <= self.max_x:
            self.expand(coord)

        self.grid[coord.y + self.origin.y][coord.x + self.origin.x] = value

    def draw(self, robot: Robot = None, path: list[Coord] = None) -> None:
        if robot:
            print(robot.position, self[robot.position])

        for r, row in list(enumerate(self.grid)):
            for c, cell in enumerate(row):
                if robot and robot.position == Coord(c, r) - self.origin:
                    print(str(robot), end='')
                elif path and Coord(c, r) - self.origin in path:
                    print('o', end='')
                else:
                    print(str(cell), end='')
            print()  # newline

    def fill_unknown(self) -> None:
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == Type.unknown:
                    self.grid[r][c] = Type.wall

    def get_neighbours(self, coord: Coord) -> list[tuple[Coord, int]]:
        return [
            (coord + HEADING[heading], 1)
            for heading in Heading
            if self.min_y <= (coord + HEADING[heading]).y <= self.max_y and
               self.min_x <= (coord + HEADING[heading]).x <= self.max_x and
               self[coord + HEADING[heading]] != Type.wall
        ]

    def find_path(self, src: Coord = None, dst: Coord = None) -> list[Coord] | None:
        """uses A* to find the shortest path between origin and oxygen"""

        def heuristic(coord: Coord) -> int:
            return 1

        if src is None:
            src = Coord(0, 0)

        if dst is None:
            dst = self.oxygen

        open_list = {src}
        closed_list = set()

        distances = {src: 0}

        parents = {src: src}

        while open_list:
            n = None

            for v in open_list:
                if n is None or distances[v] < distances[n] + heuristic(n):
                    n = v

            if n is None:
                return None

            if n == dst:
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(src)

                path.reverse()

                return path

            for (m, distance) in self.get_neighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    distances[m] = distances[n] + distance

            open_list.remove(n)
            closed_list.add(n)

    def find_distances(self, dst: Coord = None) -> dict[Coord, int]:
        """uses Dijkstra to find the shortest path starting at oxygen to all points"""

        if dst is None:
            dst = self.oxygen

        distances = {
            Coord(c, r): maxsize
            for r in range(self.min_y, self.max_y)
            for c in range(self.min_x, self.max_x)
            if self[Coord(c, r)] in (Type.empty, Type.origin, Type.oxygen)
        }

        processed = {
            Coord(c, r): False
            for r in range(self.min_y, self.max_y)
            for c in range(self.min_x, self.max_x)
            if self[Coord(c, r)] in (Type.empty, Type.origin, Type.oxygen)
        }

        distances[dst] = 0

        while not all(processed.values()):
            dist, u = min((d, p) for p, d in distances.items() if not processed[p])
            processed[u] = True

            for v, _ in self.get_neighbours(u):
                if (
                        # self[v] in (Type.empty, Type.origin, Type.oxygen) and
                        not processed[v] and
                        distances[v] > dist + 1
                ):
                    distances[v] = dist + 1

        return distances

    def load(self, data_lines: list[str]) -> None:  # manipulates grid in place
        # initialize grid once, no growing
        self.grid = [[Type.unknown for _ in range(len(data_lines[0]))] for _ in range(len(data_lines))]

        for r, row in enumerate(data_lines):
            for c, char in enumerate(row):
                cell = TYPING[char]
                if cell == Type.origin:
                    self.origin = Coord(c, r)
                    if self.oxygen:  # in case oxygen comes before origin
                        self.oxygen -= self.origin
                elif cell == Type.oxygen:
                    self.oxygen = Coord(c, r)
                    if self.origin != Coord(0, 0):  # in case origin comes before oxygen
                        self.oxygen -= self.origin

                self.grid[r][c] = cell


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def map_grid(grid: Grid, robot: Robot, verbose: bool = False, confirm: bool = False) -> None:
    if verbose:
        clear()
        grid.draw(robot)
        if confirm:
            input()

    # find the one open direction at the start and set the robot's initial heading
    for heading in Heading:
        response = robot.computer.run([heading.value])
        grid[robot.position + HEADING[heading]] = TYPE[response]
        if TYPE[response] == Type.empty:
            robot.heading = heading
            # undo the movement our robot did (in the program's memory)
            _ = robot.computer.run([heading.opposite.value])

    if verbose:
        clear()
        grid.draw(robot)
        if confirm:
            input()

    # map the maze using wall hugger algorithm (turn left when hitting a wall, right otherwise)
    # https://en.wikipedia.org/wiki/Maze-solving_algorithm#Hand_On_Wall_Rule
    while True:
        response = robot.computer.run([robot.heading.value])
        grid[robot.position + HEADING[robot.heading]] = TYPE[response]
        if TYPE[response] == Type.wall:
            robot.turn(Turn.left)
        elif TYPE[response] == Type.empty:
            robot.move()
            robot.turn(Turn.right)
        elif TYPE[response] == Type.oxygen:
            robot.move()
            robot.turn(Turn.right)
            grid.oxygen = robot.position

        if robot.position == Coord(0, 0):  # robot got back at the origin - we're done
            grid[robot.position] = Type.origin
            break

        if verbose:
            clear()
            grid.draw(robot)
            if confirm:
                input()

    grid.fill_unknown()

    if verbose:
        clear()
        grid.draw(robot)
        if confirm:
            input()


@time_it
def main(data: str, verbose: bool = False, confirm: bool = False) -> None:
    grid = Grid()
    robot = Robot(Computer(list(map(int, data.split(','))), [], False))

    map_grid(grid, robot, verbose, confirm)
    # grid.draw()
    # print(f'origin: {grid.origin} - oxygen: {grid.oxygen}')

    # grid.load(load_data(MAZE_PATH))
    # grid.draw()
    # print(f'origin: {grid.origin} - oxygen: {grid.oxygen}')

    path = grid.find_path()

    # grid.draw(path=path)

    print(f'End result: {len(path) - 1}')


if __name__ == "__main__":
    verbose = False  # default val
    confirm = False  # default value

    if '-v' in sys.argv:
        verbose = True
    if '-c' in sys.argv:
        confirm = True

    main(load_data(DATA_PATH)[0], verbose, confirm)

    # using input data:
    #   End result: 272
    #   Finished 'main' in 1.22 seconds for mapping the grid
    #   Finished 'main' in 18 milliseconds for path finding
    #   Finished 'main' in 1.22 seconds

    # # test the Grid class
    # from random import choice
    # grid = Grid([[choice(list(Type)) for _ in range(5)] for _ in range(5)])
    # # grid = Grid([[t for _ in range(5)] for t in Type])
    # robot = Robot(Computer([]), Coord(2, 2))
    # grid.draw(robot)
    # for _ in range(2):
    #     robot.move()
    #     grid.draw(robot)
    # robot.heading = Heading.south
    # grid.draw(robot)
    # for _ in range(3):
    #     robot.move()
    #     grid.draw(robot)

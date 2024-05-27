# aoc_2019_20_A_1.py - Day 20: Donut Maze - part 1
# In your maze, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ?
# https://adventofcode.com/2019/day/20


from tools import time_it

from dataclasses import dataclass, field
from enum import Enum
from string import ascii_uppercase

from pprint import pprint


DATA_PATH = './input_2019_20'


class PortalMismatch(Exception):
    pass


class Type(Enum):
    Void = ' '
    Empty = '.'
    Wall = '#'
    Portal = '*'
    Start = 'S'
    End = 'E'


@dataclass
class Coord:
    row: int
    col: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.row + other.row, self.col + other.col)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.row - other.row, self.col - other.col)

    def __neg__(self):
        return Coord(-self.row, -self.col)

    def __mul__(self, other: int) -> 'Coord':
        if not isinstance(other, int):
            raise TypeError(f'not a supported type: {type(other)}')
        return Coord(self.row * other, self.col * other)

    def __hash__(self) -> int:
        return hash((self.row, self.col))


DIRECTIONS = [
    Coord(-1, 0),  # up
    Coord(1, 0),   # down
    Coord(0, -1),  # left
    Coord(0, 1),   # right
]


@dataclass
class PortalDef:
    name: str
    coord: Coord

class Cell:
    def __str__(self):
        return Type[self.__class__.__name__].value


@dataclass
class Void(Cell):
    pass


@dataclass
class Empty(Cell):
    pass


@dataclass
class Start(Empty):
    pass


@dataclass
class End(Empty):
    pass


@dataclass
class Wall(Cell):
    pass


@dataclass
class Portal(Cell):
    target: Coord


MAZE = {
    '.': Empty(),
    '#': Wall(),
}


@dataclass
class Maze:
    rows: int
    cols: int
    start: Coord = None
    stop: Coord = None

    def __post_init__(self):
        self._maze = [[Void() for _ in range(self.cols)] for _ in range(self.rows)]

    def __getitem__(self, index: Coord) -> Cell:
        return self._maze[index.row][index.col]

    def __setitem__(self, index: Coord, value: Cell) -> None:
        self._maze[index.row][index.col] = value

    def __str__(self) -> str:
        return '\n'.join([''.join([str(c) for c in row]) for row in self._maze])

    def _get_neighbors(self, v: Coord) -> list[Coord]:
        neighbors = []

        for d in DIRECTIONS:
            if 0 <= (v + d).row < self.rows and 0 <= (v + d).col < self.cols:  # bounds check
                if isinstance(self[v + d], (Empty, Start, End, Portal)):
                    neighbors.append(v + d)
                if isinstance(self[v], Portal):
                    neighbors.append(self[v].target)

        return neighbors

    def solve(self) -> list[Coord] | None:
        open_list = {self.start}
        closed_list = set()

        distances = {self.start: 0}

        parents = {self.start: self.start}

        while open_list:
            n = None

            for v in open_list:
                if n is None or distances[v] < distances[n]:
                    n = v

            if n is None:
                return None

            if n == self.stop:
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(self.start)

                path.reverse()

                return path

            for m in self._get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    distances[m] = distances[n] + 1

                else:
                    if distances[m] > distances[n] + 1:
                        distances[m] = distances[n] + 1
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        return None


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def parse_maze(data_lines: list[str]) -> Maze:
    # instead of assuming the input file will always be padded to the full width of the maze + portal definitions
    # (PyCharm has the annoying (in this case) habit of removing trailing spaces on save), we guarantee every line
    # is padded (where it matters)
    for l, line in enumerate(data_lines[2:-2], 2):
        if all(c in MAZE for c in line[-2:]):  # no padding at all
            data_lines[l] += '  '
        elif line[-2] in MAZE:  # only space
            data_lines[l] += ' '

    maze = Maze(len(data_lines) - 4, len(data_lines[2]) - 4)
    portals: list[PortalDef] = []

    # first 2 lines contain portal names
    for c, char in enumerate(data_lines[0][2:]):
        if char in ascii_uppercase:
            portals.append(PortalDef(char + data_lines[1][c+2], Coord(0, c)))

    # last 2 lines contain portal names
    for c, char in enumerate(data_lines[-2][2:]):
        if char in ascii_uppercase:
            portals.append(PortalDef(char + data_lines[-1][c+2], Coord(len(data_lines) - 4 - 1, c)))

    # loop through rest of the input data
    for r, row in enumerate(data_lines[2:-2]):
        if not row.startswith('  '):  # portal on the left outer edge
            portals.append(PortalDef(row[:2], Coord(r, 0)))
        if not row.endswith('  '):  # portal on the right outer edge
            portals.append(PortalDef(row[-2:], Coord(r, len(data_lines[2]) - 4 - 1)))

        for c, char in enumerate(row[2:-2]):
            if char in MAZE:  # wall or empty
                maze[Coord(r,  c)] = MAZE[char]
            elif char in ascii_uppercase:  # part of portal definition
                # find the other part of the portal definition
                direction, other = [
                    (direction, data_lines[r + 2 + direction.row][c + 2 + direction.col])
                    for direction in DIRECTIONS
                    if data_lines[r + 2 + direction.row][c + 2 + direction.col] in ascii_uppercase
                ][0]

                # check whether we already created a preliminary portal
                for portal in portals:
                    if portal.name == other + char and portal.coord == Coord(-1, -1):
                        # determine portal's position
                        if direction.col == 0:  # vertical definition string
                            if data_lines[r + 2 - 2][c + 2] in MAZE:  # portal above definition
                                portal.coord = Coord(r - 2, c)
                            else:  # portal under definition
                                portal.coord = Coord(r + 1, c)
                        else:  # direction.row == 0 - horizontal definition string
                            if data_lines[r + 2][c + 2 - 2] in MAZE:  # portal left of definition
                                portal.coord = Coord(r, c - 2)
                            else:  # portal right of definition
                                portal.coord = Coord(r, c + 1)
                        break
                else:  # no matching preliminary found - create one
                    portals.append(PortalDef(char + other, Coord(-1, -1)))

    # match and place portals
    portals.sort(key=lambda p: p.name)  # sort on name of portal so portals are grouped together
    # start portal is not paired
    maze[portals[0].coord] = Start()
    maze.start = portals[0].coord
    # stop portal is not paired
    maze[portals[-1].coord] = End()
    maze.stop = portals[-1].coord
    # process the paired portals
    for first, second in zip(portals[1:-1:2], portals[2:-1:2]):
        # disable for testing
        if first.name != second.name:
            raise PortalMismatch(f'portals don\'t match: {first.name} != {second.name}')

        maze[first.coord] = Portal(second.coord)
        maze[second.coord] = Portal(first.coord)

    return maze


# test_data = ['test_data_01_bis', 'test_data_02',]
test_data = ['test_data_01', 'test_data_02',]


@time_it
def main(data_lines: list[str]) -> None:
    maze = parse_maze(data_lines)
    # print(maze)

    path = maze.solve()
    # pprint(path)

    if path is None:
        print('No solution found.')
    else:
        print(f'End result: {len(path) - 1}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(load_data(test_data[0]))
    # main(load_data(test_data[1]))

    # using test_data[0]:
    #   End result: 23
    #   Finished 'main' in 1 millisecond
    # using test_data[1]:
    #   End result: 58
    #   Finished 'main' in 4 milliseconds
    # using input data:
    #   End result: 684
    #   Finished 'main' in 78 milliseconds

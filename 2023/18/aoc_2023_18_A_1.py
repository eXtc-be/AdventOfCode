#! /usr/bin/python3

# aoc_2023_18_A_1.py - Day 18: Lavaduct Lagoon - part 1
# The Elves are concerned the lagoon won't be large enough;
# if they follow their dig plan, how many cubic meters of lava could it hold?
# https://adventofcode.com/2023/day/18

from tools import time_it

from typing import NamedTuple
from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2023_18'

HEX_CHARS = '0123456789ABCDEF'

DIRECTIONS: dict[str, tuple[int, int]] = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

DIR_TO_WALL: dict[str, str] = {
    'U': '│',
    'D': '│',
    'L': '─',
    'R': '─',
    'UL': '┐',
    'UR': '┌',
    'DL': '┘',
    'DR': '└',
    'LU': '└',
    'RU': '┘',
    'LD': '┌',
    'RD': '┐',
}

# formatting codes
COLOR_FORMAT = '\033[38;2;{};{};{}m'

HEADER = '\033[95m'  # (magenta)
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'  # (orange)
FAIL = '\033[91m'  # (red)

BOLD = '\033[1m'
UNDERLINE = '\033[4m'

ENDC = '\033[0m'


@dataclass
class Coord:
    row: int
    col: int

    def __add__(self, other):
        return Coord(self.row + other.row, self.col + other.col)

    def __mul__(self, factor):
        return Coord(self.row * factor, self.col * factor)


@dataclass
class Direction:
    name: str
    delta: Coord = field(init=False)

    def __post_init__(self):
        if self.name not in DIRECTIONS:
            raise ValueError('invalid direction: {}'.format(self.name))

        self.delta = Coord(*DIRECTIONS[self.name])


class Color(NamedTuple):
    r: int = 0
    g: int = 0
    b: int = 0

    @classmethod
    def from_hex(cls, hex_str: str) -> 'Color':
        if len(hex_str) != 7:
            raise ValueError('invalid hex color value: {}'.format(hex_str))
        if hex_str[0] != '#':
            raise ValueError('invalid hex color value: {}'.format(hex_str))
        for c in hex_str[1:]:
            if c.upper() not in HEX_CHARS:
                raise ValueError('invalid hex color value: {}'.format(hex_str))

        r = HEX_CHARS.index(hex_str[1].upper()) * 16 + HEX_CHARS.index(hex_str[2].upper())
        g = HEX_CHARS.index(hex_str[3].upper()) * 16 + HEX_CHARS.index(hex_str[4].upper())
        b = HEX_CHARS.index(hex_str[5].upper()) * 16 + HEX_CHARS.index(hex_str[6].upper())

        return cls(r, g, b)

    @classmethod
    def from_dec(cls, dec_val: int) -> 'Color':
        r, g = divmod(dec_val, 256*256)
        g, b = divmod(g, 256)

        if any(c > 256 for c in [r, g, b]):
            raise ValueError('invalid decimal color value: {}'.format(dec_val))

        return cls(r, g, b)

    @property
    def hex(self):
        return (f'#'
                f'{HEX_CHARS[self.r//16]}{HEX_CHARS[self.r%16]}'
                f'{HEX_CHARS[self.g//16]}{HEX_CHARS[self.g%16]}'
                f'{HEX_CHARS[self.b//16]}{HEX_CHARS[self.b%16]}')

    @property
    def dec(self):
        return (self.r * 256 + self.g) * 256 + self.b


class Instruction(NamedTuple):
    direction: Direction
    value: int
    color: Color


@dataclass
class Cell:
    color: Color = Color()
    depth: int = 0
    wall: str = '.'

    def __str__(self) -> str:
        return COLOR_FORMAT.format(self.color.r, self.color.g, self.color.b) + str(self.wall) + ENDC


@dataclass
class Row:
    num_cols: int = 1
    cells: list[Cell] = field(default_factory=list)

    def __post_init__(self):
        if not self.cells:
            self.cells = [Cell() for _ in range(self.num_cols)]

    def grow(self, num_cols):
        # DONE: allow negative number to grow left
        new_cells = [Cell() for _ in range(abs(num_cols))]
        if num_cols > 0:
            self.cells = self.cells + new_cells
        else:
            self.cells = new_cells + self.cells
        self.num_cols += abs(num_cols)

    @classmethod
    def from_string(cls, string: str) -> 'Row':
        cells = [Cell(Color(int(char != '.')*255, 0, 0 ), int(char != '.'), char) for char in string]
        return cls(len(cells), cells)

    def _find_edges(self):
        """marks all cells in the row that are considered an edge"""
        edges = []

        prev = ''
        for cell in self:
            if cell.depth == 0:
                edges.append(' ')
                continue  # skip if this cell isn't part of the loop

            if cell.wall == '│':
                edges.append('E')  # in/out status changed
            elif cell.wall == '─':
                edges.append('-')  # in/out status not changed, condition for next edge not changed
            elif cell.wall == '┌':
                edges.append(' ')
                prev = cell.wall  # in/out status changed, condition for next edge changed
            elif cell.wall == '└':
                edges.append(' ')
                prev = cell.wall  # in/out status changed, condition for next edge changed
            elif cell.wall == '┘':
                if prev in list('┌'):
                    edges.append('E')
                else:
                    edges.append(' ')
                prev = cell.wall  # in/out status changed, condition for next edge changed
            elif cell.wall == '┐':
                if prev in list('└'):
                    edges.append('E')
                else:
                    edges.append(' ')
                prev = cell.wall  # in/out status changed, condition for next edge changed
            else:
                edges.append(' ')

        return edges

    def dig_out(self) -> None:
        # print(''.join([cell.wall for cell in self.cells]))

        edges = self._find_edges()
        # print(''.join(edges))

        last_color = Color()

        # cells in the first and last rows and columns can only be part of the loop or outside the loop,
        # so we don't bother to check those
        for c, cell in enumerate(self[1:-1], 1):
            if cell.depth == 0:
                left, right = edges[:c], edges[c+1:]
                if left.count('E') % 2 == 1 and right.count('E') % 2 == 1:
                    cell.depth = 1
                    cell.color = last_color
                    cell.wall = '░'
            else:
                last_color = cell.color

        # print(''.join([cell.wall for cell in self.cells]))
        # row.cells[i].color = row.cells[start].color
        # row.cells[i].depth += 1

    @property
    def active(self) -> int:
        return len([cell for cell in self.cells if cell.depth > 0])

    def __len__(self):
        return self.num_cols

    def __getitem__(self, index):
        return self.cells[index]

    def __setitem__(self, index, value):
        self.cells[index] = value

    def __str__(self) -> str:
        return ''.join(str(cell) for cell in self.cells)


@dataclass
class Grid:
    num_rows: int = 1
    num_cols: int = 1
    rows: list[Row] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.rows:
            self.rows = [Row(self.num_cols) for _ in range(self.num_rows)]

    def grow(self, num_rows=0, num_cols=0) -> None:
        # DONE: allow negative numbers to grow up/left
        if num_cols:
            for row in self.rows:
                row.grow(num_cols)
        self.num_cols = self.rows[0].num_cols
        if num_rows:
            new_rows = [Row(len(self.rows[0])) for _ in range(abs(num_rows))]
            if num_rows > 0:
                self.rows = self.rows + new_rows
            else:
                self.rows = new_rows + self.rows
            self.num_rows += abs(num_rows)

    @classmethod
    def from_string(cls, string: str) -> 'Grid':
        rows = [Row.from_string(line) for line in string.strip().splitlines()]
        return cls(len(rows), rows[0].num_cols, rows)

    def follow_instructions(self, instructions: list[Instruction]) -> None:  # changes the grid in place
        # DONE: make this a class method
        current_position = Coord(0, 0)
        self[current_position].wall = '░'
        previous_move = ''
        for instruction in instructions:
            move = instruction.direction.name
            delta = instruction.direction.delta
            value = instruction.value
            color = instruction.color

            if current_position.col + delta.col * (value + 0) < 0:
                self.grow(0, current_position.col + delta.col * (value + 0))
                current_position.col -= current_position.col + delta.col * (value + 0)
            elif current_position.col + delta.col * (value + 1) > self.num_cols:
                self.grow(0, current_position.col + delta.col * (value + 1) - self.num_cols)

            if current_position.row + delta.row * (value + 0) < 0:
                self.grow(current_position.row + delta.row * (value + 0), 0)
                current_position.row -= current_position.row + delta.row * (value + 0)
            elif current_position.row + delta.row * (value + 1) > self.num_rows:
                self.grow(current_position.row + delta.row * (value + 1) - self.num_rows, 0)

            if previous_move:
                self[current_position].wall = DIR_TO_WALL[previous_move + move]

            if delta.col:
                for _ in range(value):
                    current_position.col += delta.col
                    self[current_position].color = color
                    self[current_position].depth = 1
                    self[current_position].wall = DIR_TO_WALL[move]

            if delta.row:
                for _ in range(value):
                    current_position.row += delta.row
                    self[current_position].color = color
                    self[current_position].depth = 1
                    self[current_position].wall = DIR_TO_WALL[move]

            previous_move = move

            # print(self)

        # change first/last corner
        # self[current_position].wall = '░'
        self[current_position].wall = DIR_TO_WALL[previous_move + instructions[0].direction.name]

    def dig_out(self) -> None:  # changes the grid in place
        # DONE: make this a class method
        # cells in the first and last rows and columns can only be part of the loop or be outside the loop,
        # so we don't bother to check those rows 0 and -1
        # for row in self:
        for row in self[1:-1]:
            row.dig_out()

    @property
    def active(self) -> int:
        return sum(row.active for row in self.rows)

    def __len__(self) -> int:
        return self.num_rows

    def __getitem__(self, index: Coord | int) -> Cell | Row:
        if isinstance(index, Coord):
            return self.rows[index.row][index.col]
        else:
            return self.rows[index]

    def __setitem__(self, index: Coord | int, value: Cell) -> None:
        if isinstance(index, Coord):
            self.rows[index.row][index.col] = value
        else:
            for cell in self.rows[index]:
                cell[index] = value

    def __str__(self) -> str:
        return '\n'.join(str(row) for row in self.rows)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_instructions(data_lines: list[str]) -> list[Instruction]:
    return [
        Instruction(
            Direction(line.split()[0].upper()),
            int(line.split()[1]),
            Color.from_hex(line.split()[2][1:-1])
        )
        for line in data_lines
    ]


# test_data = '''
# L 6 (#70c710)
# U 5 (#0dc571)
# R 2 (#5713f0)
# U 2 (#d2c081)
# L 2 (#59c680)
# U 2 (#411b91)
# R 5 (#8ceee2)
# D 2 (#caa173)
# R 1 (#1b58a2)
# D 2 (#caa171)
# L 2 (#7807d2)
# D 3 (#a77fa3)
# R 2 (#015232)
# D 2 (#7a21e3)
# '''.strip().splitlines()

# test_data = '''
# R 10 (#000000)
# D 4 (#000000)
# L 2 (#000000)
# U 2 (#000000)
# L 2 (#000000)
# D 3 (#000000)
# L 2 (#000000)
# U 3 (#000000)
# L 2 (#000000)
# D 2 (#000000)
# L 2 (#000000)
# U 4 (#000000)
# '''.strip().splitlines()

test_data = '''
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''.strip().splitlines()


test_grid = """
...│...│..└─┐..┌─┐..┌─┘.│.....│.│.│.└─┘
"""


@time_it
def main(data_lines: list[str]) -> None:
    grid = Grid()

    instructions = get_instructions(data_lines)
    # pprint(instructions)

    grid.follow_instructions(instructions)
    # print(grid)
    # print(grid.active)

    grid.dig_out()
    # print(grid)
    # print(grid.active)

    print(f'End result: {grid.active}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 62
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 70026
    #   Finished 'main' in 1.07 seconds

    # # test class Direction
    # print(Direction('U'))
    # print(Direction('R'))
    # # print(Direction('X'))  # ValueError

    # # test class Color
    # print(Color(5, 5, 5))
    # print(Color.from_hex('#AB10EF'))
    # # print(Color.from_hex('AB10EF'))  # ValueError
    # # print(Color.from_hex('AB10EF1'))  # ValueError
    # # print(Color.from_hex('#AB1GEF'))  # ValueError
    # print(Color.from_dec(328965))
    # # print(Color.from_dec(100000000))  # ValueError
    # print(Color(5, 15, 105).hex)
    # print(Color(5, 5, 5).dec)

    # # test class Row
    # row = Row()
    # pprint(row)
    # row.grow(2)
    # pprint(row)
    # row[0].color = Color(128, 0, 0)
    # row.grow(-3)
    # pprint(row)

    # # test class Grid
    # grid = Grid(5, 5)
    # grid[Coord(0, 0)] = Cell(Color(255, 0, 0))
    # grid[Coord(0, 1)] = Cell(Color(0, 255, 0))
    # grid[Coord(0, 2)] = Cell(Color(0, 0, 255))
    # grid[Coord(0, 3)] = Cell(Color(128, 0, 0))
    # grid[Coord(0, 4)] = Cell(Color(0, 128, 255))
    # print(grid)
    #
    # # grid = Grid()
    # # print(grid)
    # grid.grow(0, 2)
    # print(grid)
    # grid.grow(2, 0)
    # print(grid)
    # grid.grow(-3, -5)
    # print(grid)
    # grid[Coord(0, 0)] = Cell(Color(128, 0, 0))
    # print(grid[Coord(0, 0)].color.hex)
    # print(grid[Coord(3, 3)].depth)

    # # test Row.from_string
    # row = Row.from_string('0011001010')
    # print(row)

    # # test Grid.from_string
    # grid = Grid.from_string(test_grid)
    # print(grid)

    # # test dig_out
    # grid = Grid.from_string(test_grid)
    # print(grid)
    # grid.rows[0].dig_out()
    # print(grid)

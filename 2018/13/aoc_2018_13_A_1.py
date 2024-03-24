# aoc_2018_13_A_1.py - Day 13: Mine Cart Madness - part 1
# What is the location of the first crash?
# https://adventofcode.com/2018/day/13
# first version: in an effort to keep the memory usage low I decided to keep a flat list of track sections,
# each with its own coordinate, skipping empty cells
# the problem with this approach is that on every tick, for every cart I have to loop through the entire list
# to find that cart's next section, which is extremely slow, especially near the bottom of the grid:
#   doing a mere 150 ticks takes more than 8 seconds!


from tools import time_it

from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import cycle

from pprint import pprint


DATA_PATH = './input_2018_13'

# other constants


class Type(Enum):
    NS = auto()  # vertical             |
    EW = auto()  # horizontal           -
    SE = auto()  # corner down & right  F (/)
    SW = auto()  # corner down & left   7 (\)
    NE = auto()  # corner up & right    L (\)
    NW = auto()  # corner up & left     J (/)
    X = auto()   # crossing    +


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class Section:
    location: Point
    type: Type

    def __str__(self):
        return DRAW_TRACK[self.type]


@dataclass
class Cart:
    location: Point
    heading: str

    def __post_init__(self):
        self.moves = cycle(MOVES)

    def __str__(self):
        return DRAW_CART[self.heading]


@dataclass
class Track:
    sections: list[Section] = field(default_factory=list)
    carts: list[Cart] = field(default_factory=list)
    draw_carts: bool = True
    collision: Point = None

    def __post_init__(self):
        self.tick = 0

    def do_tick(self) -> None:
        """
        moves all carts 1 cell in the direction they are facing, changing directions as needed
        sets the location of a crash if one occurred
        """
        # increment tick counter
        self.tick += 1

        # loop through all carts and move them 1 cell
        for cart in sorted(self.carts, key=lambda c: (c.location.y, c.location.x)):
            cart.location = cart.location + DIRECTIONS[cart.heading]
            match [section for section in self.sections if section.location == cart.location][0].type:
                case Type.SE:
                    cart.heading = 'E' if cart.heading == 'N' else 'S'
                case Type.SW:
                    cart.heading = 'W' if cart.heading == 'N' else 'S'
                case Type.NE:
                    cart.heading = 'E' if cart.heading == 'S' else 'N'
                case Type.NW:
                    cart.heading = 'W' if cart.heading == 'S' else 'N'
                case Type.X:
                    cart.heading = HEADINGS[cart.heading][next(cart.moves)]
                case _:
                    pass  # don't change cart's heading

        # loop through all carts and check if any has the same location as another one
        for cart in self.carts:
            if cart.location in [c.location for c in self.carts if c != cart]:
                self.collision = cart.location
                return

    def __str__(self):
        lines = []

        for r in range(max(section.location.y for section in self.sections) + 1):
            sections = [section for section in self.sections if section.location.y == r]
            line = [' '] * (max(section.location.x for section in sections) + 1)
            for section in sections:
                line[section.location.x] = str(section)
            if self.draw_carts:
                carts = [cart for cart in self.carts if cart.location.y == r]
                for cart in carts:
                    if cart.location == self.collision:
                        line[cart.location.x] = COLLISION
                    else:
                        line[cart.location.x] = str(cart)
            lines.append(''.join(line))

        return '\n'.join(lines)


TYPE = {  # translates input characters to track Types
    '|': Type.NS,
    '-': Type.EW,
    '+': Type.X,
    '^': Type.NS,
    'v': Type.NS,
    '<': Type.EW,
    '>': Type.EW,
}

CART = {  # translates input characters to Headings
    '^': 'N',
    'v': 'S',
    '<': 'W',
    '>': 'E',
}

DIRECTIONS = {  # translates a heading to a coordinate
    'N': Point(0, -1),
    'E': Point(1, 0),
    'S': Point(0, 1),
    'W': Point(-1, 0),
}

HEADINGS = {  # translates a heading and a turn into a new heading
    'N': {'L': 'W', 'S': 'N', 'R': 'E'},
    'E': {'L': 'N', 'S': 'E', 'R': 'S'},
    'S': {'L': 'E', 'S': 'S', 'R': 'W'},
    'W': {'L': 'S', 'S': 'W', 'R': 'N'},
}

MOVES = ['L', 'S', 'R']  # the different moves of a cart in order (repeats forever)

DRAW_TRACK = {  # for drawing a track with box drawing symbols
    Type.NS: '│',
    Type.EW: '─',
    Type.SE: '┌',
    Type.SW: '┐',
    Type.NE: '└',
    Type.NW: '┘',
    Type.X: '┼',
}

DRAW_CART = {  # for drawing a cart with arrow heads
    'N': '▲',
    'E': '►',
    'S': '▼',
    'W': '◄',
}

COLLISION = 'X'
# COLLISION = '▒'
# COLLISION = '☼'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def read_input(data_lines: list[str]) -> Track:
    track = Track()  # create an empty track

    for r, line in enumerate(data_lines):
        for c, cell in enumerate(line):
            # determine the track type and add to track's sections list
            if cell in TYPE:
                track.sections.append(Section(Point(c, r), TYPE[cell]))
            elif cell == '/':
                if c > 0 and line[c-1] in '-+':
                    track.sections.append(Section(Point(c, r), Type.NW))
                else:
                    track.sections.append(Section(Point(c, r), Type.SE))
            elif cell == '\\':
                if c > 0 and line[c-1] in '-+':
                    track.sections.append(Section(Point(c, r), Type.SW))
                else:
                    track.sections.append(Section(Point(c, r), Type.NE))

            # determine the cart type and add to track's carts list
            if cell in CART:
                track.carts.append(Cart(Point(c, r), CART[cell]))

    return track


# test_data = r'''
# /----\
# |    |
# |    |
# \----/
# '''.strip().splitlines()

# test_data = r'''
# /-----\
# |     |
# |  /--+--\
# |  |  |  |
# \--+--/  |
#    |     |
#    \-----/
# '''.strip().splitlines()

# test_data = r'''
# /-->--\
# |     |
# |  /--+--\
# |  |  |  |
# \--+--/  |
#    |     |
#    \-----/
# '''.strip().splitlines()

# test_data = r'''
# /->--\
# |    |
# |    |
# \----/
# '''.strip().splitlines()

# test_data = r'''
# |
# v
# |
# |
# |
# ^
# |
# '''.strip().splitlines()

# test_data = r'''
# /->--\
# |    |
# |    |
# \->--/
# '''.strip().splitlines()

# test_data = r'''
# /->--\
# |    |
# |    |
# \-->-/
# '''.strip().splitlines()

test_data = r'''
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], verbose: bool = False) -> None:
    track = read_input(data_lines)
    if verbose:
        print(track.tick)
        print(track)
        print('-' * 100)
    else:
        print(track.tick)

    while True:
        track.do_tick()
        if verbose:
            print(track.tick)
            print(track)
            print('-' * 100)
        else:
            if track.tick % 10 == 0:
                print(track.tick)

        if track.collision:
            break

    print(f'End result: {track.collision.x},{track.collision.y} in {track.tick} ticks')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)
    # main(test_data, verbose=True)

    # using test_data:
    #   End result: 7,3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 136,31 - not correct
    #   Finished 'main' in 8.5 seconds

    # test Track.__str__
    # print(Track([
    #     Section(Point(0, 0), Type.SE),
    #     Section(Point(1, 0), Type.EW),
    #     Section(Point(2, 0), Type.SW),
    #
    #     Section(Point(0, 1), Type.NS),
    #     Section(Point(1, 1), Type.SE),
    #     Section(Point(2, 1), Type.X),
    #     Section(Point(3, 1), Type.SW),
    #
    #     Section(Point(0, 2), Type.NE),
    #     Section(Point(1, 2), Type.X),
    #     Section(Point(2, 2), Type.NW),
    #     Section(Point(3, 2), Type.NS),
    #
    #     Section(Point(1, 3), Type.NE),
    #     Section(Point(2, 3), Type.EW),
    #     Section(Point(3, 3), Type.NW),
    # ]))

    # print(Track([
    #     Section(Point(0, 0), Type.SE),
    #     Section(Point(1, 0), Type.EW),
    #     Section(Point(2, 0), Type.EW),
    #     Section(Point(3, 0), Type.EW),
    #     Section(Point(4, 0), Type.SW),
    #
    #     Section(Point(0, 1), Type.NS),
    #     Section(Point(4, 1), Type.NS),
    #
    #     Section(Point(0, 2), Type.NS),
    #     Section(Point(2, 2), Type.SE),
    #     Section(Point(3, 2), Type.EW),
    #     Section(Point(4, 2), Type.X),
    #     Section(Point(5, 2), Type.EW),
    #     Section(Point(6, 2), Type.SW),
    #
    #     Section(Point(0, 3), Type.NS),
    #     Section(Point(2, 3), Type.NS),
    #     Section(Point(4, 3), Type.NS),
    #     Section(Point(6, 3), Type.NS),
    #
    #     Section(Point(0, 4), Type.NE),
    #     Section(Point(1, 4), Type.EW),
    #     Section(Point(2, 4), Type.X),
    #     Section(Point(3, 4), Type.EW),
    #     Section(Point(4, 4), Type.NW),
    #     Section(Point(6, 4), Type.NS),
    #
    #     Section(Point(2, 5), Type.NS),
    #     Section(Point(6, 5), Type.NS),
    #
    #     Section(Point(2, 6), Type.NE),
    #     Section(Point(3, 6), Type.EW),
    #     Section(Point(4, 6), Type.EW),
    #     Section(Point(5, 6), Type.EW),
    #     Section(Point(6, 6), Type.NW),
    # ]))


# aoc_2018_13_A_2.py - Day 13: Mine Cart Madness - part 1
# What is the location of the first crash?
# https://adventofcode.com/2018/day/13
# second version: track sections are now stored in a 2-dimensional grid, so looking up a cart's next
# section is near instant, no matter where in the grid it is. this version finishes in 28 milliseconds

import sys
sys.path.append('../..')

from tools import time_it

from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import cycle
import os

from pprint import pprint


DATA_PATH = './input_2018_13'

# other constants


class Type(Enum):
    NO = auto()  # empty section
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
    type: Type

    def __str__(self):
        return DRAW_TRACK[self.type]


@dataclass
class Cart:
    location: Point
    heading: str
    id: int
    # new_location: Point = None

    def __post_init__(self):
        self.moves = cycle(MOVES)
        self.crashed = False

    def __str__(self):
        return DRAW_CART[self.heading]


@dataclass
class Track:
    sections: list[list[Section]] = field(default_factory=list)
    carts: list[Cart] = field(default_factory=list)
    draw_carts: bool = True

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
            if cart.crashed:
                continue
            cart.location = cart.location + DIRECTIONS[cart.heading]
            match self.sections[cart.location.y][cart.location.x].type:
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
            for crt in self.carts:
                if crt.location in [c.location for c in self.carts if c is not crt]:
                    crt.crashed = True

    def remove_collided(self) -> None:
        to_remove = [cart for cart in self.carts if cart.crashed]
        for cart in to_remove:
            print(f'Cart {cart.id} crashed at {cart.location} on tick {self.tick}')
            self.carts.remove(cart)
        if len(self.carts) > 1:
            print(f'{len(self.carts)} carts left')

    def __str__(self):
        track = [[str(section) for section in sections] for sections in self.sections]
        if self.draw_carts:
            for cart in self.carts:
                if cart.crashed:
                    track[cart.location.y][cart.location.x] = COLLISION
                else:
                    track[cart.location.y][cart.location.x] = str(cart)
        return f'Tick: {self.tick}\n' + '\n'.join(''.join(map(str, sections)) for sections in track)


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
    Type.NO: ' ',
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
    max_x = max(len(line) for line in data_lines)
    max_y = len(data_lines)

    track = Track()  # create an empty track

    track.sections = [[Section(Type.NO) for _ in range(max_x)] for _ in range(max_y)]

    cart_id = 1

    for r, line in enumerate(data_lines):
        for c, cell in enumerate(line):
            # determine the track type and add to track's sections list
            if cell in TYPE:
                track.sections[r][c] = Section(TYPE[cell])
            elif cell == '/':
                if c > 0 and line[c-1] in '-+^v<>':
                    track.sections[r][c] = Section(Type.NW)
                else:
                    track.sections[r][c] = Section(Type.SE)
            elif cell == '\\':
                if c > 0 and line[c-1] in '-+^v<>':
                    track.sections[r][c] = Section(Type.SW)
                else:
                    track.sections[r][c] = Section(Type.NE)

            # determine the cart type and add to track's carts list
            if cell in CART:
                track.carts.append(Cart(Point(c, r), CART[cell], cart_id))
                cart_id += 1

    return track


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear') if not os.environ.get('CHARM') else print('-' * 100)


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
def main(data_lines: list[str], step: bool = False, verbose: bool = False) -> None:
    track = read_input(data_lines)
    # pprint(track)
    if verbose:
        print(track)
        # print('-' * 100)
    else:
        print(track.tick)

    while True:
        track.do_tick()
        if verbose:
            clear()
            print(track)
            # print('-' * 100)
        else:
            if track.tick % 100 == 0:
                print(track.tick)

        crash = None
        for cart in track.carts:
            if cart.crashed:
                crash = cart.location
                break

        if crash:
            break

        if step:
            input('Press Enter to continue')

    print(f'End result: {crash.x},{crash.y} in {track.tick} ticks')


if __name__ == "__main__":
    main(load_data(DATA_PATH), step=False, verbose=False)
    # main(test_data)
    # main(test_data, step=True, verbose=True)

    # using test_data:
    #   End result: 7,3 in 14 ticks
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 136,36 in 145 ticks
    #   Finished 'main' in 176 milliseconds

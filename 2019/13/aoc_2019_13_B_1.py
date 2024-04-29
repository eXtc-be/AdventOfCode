# aoc_2019_13_B_1.py - Day 13: Care Package - part 2
# What is your score after the last block is broken?
# https://adventofcode.com/2019/day/13


import sys
sys.path.extend(['.', '..', '../..'])

from aoc_2019_13_A_1 import (
    DATA_PATH,
    load_data,
)

from tools import time_it, clear
from intcode import Computer, State

from dataclasses import dataclass, field
from enum import Enum
from time import sleep

from pprint import pprint


@dataclass
class Coord:
    x: int = 0
    y: int = 0

    def __hash__(self):
        return hash((self.x, self.y))


class Tile(Enum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4

    def __str__(self):
        return TILES[self]


TILE = {
    0: Tile.empty,
    1: Tile.wall,
    2: Tile.block,
    3: Tile.paddle,
    4: Tile.ball,
}


TILES = {
    Tile.empty: ' ',
    Tile.wall: '█',
    Tile.block: '░',
    Tile.paddle: '─',
    Tile.ball: '●',
}


class Stick(Enum):
    left = -1
    neutral = 0
    right = 1


STICK = {
    -1: Stick.left,
    0: Stick.neutral,
    1: Stick.right,
}


@dataclass
class Grid:
    tiles: list[list[Tile]] = field(default_factory=list)
    score: int = 0

    def __post_init__(self) -> None:
        self.tiles = [[Tile.empty]]

    @property
    def max_y(self) -> int:
        return len(self.tiles) - 1

    @property
    def max_x(self) -> int:
        return len(self.tiles[0]) - 1

    def expand(self, coord: Coord) -> None:
        if coord.y > self.max_y:  # grow vertically
            for _ in range(coord.y - self.max_y):
                self.tiles.append([Tile.empty for c in range(len(self.tiles[0]))])
        if coord.x > self.max_x:  # grow horizontally
            for _ in range(coord.x - self.max_x):
                for row in self.tiles:
                    row.append(Tile.empty)

    def __getitem__(self, coord: Coord) -> Tile:
        if coord.y > self.max_y or coord.x > self.max_x:
            self.expand(coord)

        return self.tiles[coord.y][coord.x]

    def __setitem__(self, coord: Coord, tile: Tile):
        if coord.y > self.max_y or coord.x > self.max_x:
            self.expand(coord)

        self.tiles[coord.y][coord.x] = tile

    def draw(self) -> None:
        print(f'Score: {self.score}')
        for r, row in list(enumerate(self.tiles)):
            for c, tile in enumerate(row):
                print(str(tile), end='')
            print()  # newline


# other functions


@time_it
def main(data: str, verbose: bool = False, confirm: bool = False) -> None:
    ball: Coord = Coord(0, 0)
    paddle: Coord = Coord(0, 0)
    stick: Stick = Stick.neutral

    grid: Grid = Grid()

    computer: Computer = Computer(list(map(int, data.split(','))), [], False)
    computer.memory[0] = 2

    computer.run()

    while computer.state != State.halted:
        # take 3 output values at a time and process them
        for x, y, t in zip(*[iter(computer.outputs)] * 3):
            if (x, y) == (-1, 0):
                grid.score = t
            else:
                grid[Coord(x, y)] = TILE[t]

            if t == Tile.ball.value:
                ball = Coord(x, y)

            if t == Tile.paddle.value:
                paddle = Coord(x, y)

        if verbose:
            clear()
            grid.draw()

            if confirm:
                input()

        if ball.x < paddle.x:
            stick = stick.left
        elif ball.x > paddle.x:
            stick = stick.right
        else:
            stick = stick.neutral

        computer.outputs = []
        computer.run([stick.value])  # resume the program with an input value for the joystick

    # print(computer.state)

    # print(computer.outputs)

    print(f'End result: {computer.outputs[-1]}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0], False)
    # main(load_data(DATA_PATH)[0], True)

    # using input data:
    #   End result: 13331
    #   Finished 'main' in 3 minutes and 49 seconds (verbose = True)
    #   Finished 'main' in 1 minute and 37 seconds (verbose = True; clearing outputs)
    #   Finished 'main' in 1 minute and 59 seconds (verbose = False)
    #   Finished 'main' in 4.3 seconds (verbose = False; clearing outputs)

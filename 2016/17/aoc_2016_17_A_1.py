# aoc_2016_17_A_1.py - Day 17: Two Steps Forward - part 1
# What is the shortest path (the actual path, not just the length) to reach the vault?
# https://adventofcode.com/2016/day/17


from tools import time_it

import hashlib
from typing import NamedTuple
from dataclasses import dataclass, field

from pprint import pprint

DATA_PATH = './input_2016_17'

ROWS, COLS = 4, 4


class Point(NamedTuple):
    x: int
    y: int


DIRECTIONS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
}

OPEN = 'bcdef'


@dataclass
class Room:
    row: int
    col: int
    doors: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self):
        self.doors = {
            direction: (0 <= self.row + displacement.y <= ROWS - 1) and (0 <= self.col + displacement.x <= COLS - 1)
            for direction, displacement in DIRECTIONS.items()
        }


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_rooms() -> list[Room]:
    return [
        Room(row, col)
        for row in range(ROWS) for col in range(COLS)
    ]


def find_room(rooms: list[Room], row: int, col: int) -> Room:
    return [room for room in rooms if room.row == row and room.col == col][0]


def get_doors(passcode: str) -> list[tuple[str, bool]]:
    code = hashlib.md5(bytes(passcode, 'ascii')).hexdigest()[:4]
    return [(direction, code[i] in OPEN) for i, direction in enumerate(DIRECTIONS)]


def find_all_paths(rooms: list[Room], start_code: str, start_room: Room, start_path: str) -> list[str]:
    paths = []

    while True:
        open_doors = [
            door
            for door, is_open in get_doors(start_code + start_path)
            if is_open and start_room.doors[door]
        ]
        # print(open_doors)

        for door in open_doors:
            # check if any of the open doors leads to the vault
            if (start_room.row + DIRECTIONS[door].y == ROWS - 1 and
                    start_room.col + DIRECTIONS[door].x == COLS - 1):
                paths += [start_path + door]
            else:
                new_room = find_room(
                    rooms,
                    start_room.row + DIRECTIONS[door].y,
                    start_room.col + DIRECTIONS[door].x
                )
                new_path = start_path + door

                new_paths = find_all_paths(rooms, start_code, new_room, new_path)
                for path in new_paths:
                    paths += [path]

        return paths


test_data = '''
hijkl
ihgpwlah
kglvqrro
ulqzkmiv
'''.strip().splitlines()


@time_it
def main(start_code: str) -> None:
    rooms = create_rooms()
    # pprint(rooms)

    all_paths = find_all_paths(
        rooms,
        start_code,
        find_room(rooms, 0, 0),
        ''
    )  # find all paths starting with room in upper left corner
    # pprint(all_paths)

    if all_paths:
        print(f'End result: {min(all_paths, key=lambda p: len(p))}')
    else:
        print('No solution found')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # using test_data hijkl:
    #   End result: No solution found
    #   Finished 'main' in less than a millisecond
    # using test_data ihgpwlah:
    #   End result: DDRRRD
    #   Finished 'main' in 169 milliseconds
    # using test_data kglvqrro:
    #   End result: DDUDRLRRUDRD
    #   Finished 'main' in 274 milliseconds
    # using test_data ulqzkmiv:
    #   End result: DRURDRUDDLLDLUURRDULRLDUUDDDRR
    #   Finished 'main' in 293 milliseconds
    # using input data:
    #   End result: DRLRDDURDR
    #   Finished 'main' in 182 milliseconds

    # # test get_doors
    # print(get_doors('hijkl'))
    # print(get_doors('hijklD'))
    # print(get_doors('hijklDR'))
    # print(get_doors('hijklDU'))
    # print(get_doors('hijklDUR'))

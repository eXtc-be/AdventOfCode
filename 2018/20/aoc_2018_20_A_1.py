# aoc_2018_20_A_1.py - Day 20: A Regular Map - part 1
# What is the largest number of doors you would be required to pass through to reach a room?
# https://adventofcode.com/2018/day/20


from tools import time_it

from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict

from pprint import pprint


DATA_PATH = './input_2018_20'

# other constants


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Tristate(Enum):
    yes = auto()
    no = auto()
    maybe = auto()

    def __repr__(self):
        return self.name


class Direction(Enum):
    N = Point(0, 1)
    E = Point(1, 0)
    S = Point(0, -1)
    W = Point(-1, 0)

    def __repr__(self):
        return self.name


DIRECTIONS = {
    'N': Direction.N,
    'E': Direction.E,
    'S': Direction.S,
    'W': Direction.W,
}

OPPOSITE = {
    Direction.N: Direction.S,
    Direction.E: Direction.W,
    Direction.S: Direction.N,
    Direction.W: Direction.E,
}

WALL = '#'
ROOM = '.'
CURRENT = 'X'
POS = 'x'
EMPTY = ' '

DOORS_TRI = {
    Tristate.yes: '/',
    Tristate.no: WALL,
    Tristate.maybe: '?',
}

DOORS = {
    Direction.N: '-',
    Direction.E: '|',
    Direction.S: '-',
    Direction.W: '|',
}


@dataclass
class Room:
    position: Point
    doors: dict[Direction, Tristate] = field(default_factory=dict)

    def __repr__(self):
        return f'Room{self.position}: [' + ', '.join([f'{repr(direction)}: {DOORS_TRI[door]}' for direction, door in self.doors.items()]) + ']'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_rooms(data: str) -> tuple[list[Room], dict[Point, int]]:
    assert data[0] == '^' and data[-1] == '$' and data.count('^') == 1 and data.count('$') == 1

    rooms = []
    stack = []
    distances = defaultdict(int)

    previous_position, new_position = None, None

    current_room = Room(Point(0, 0), {d: Tristate.maybe for d in Direction})

    rooms.append(current_room)
    # print('\n'.join(''.join(char for char in row) for row in construct_maze(rooms)) + '\n' + '-' * 100)

    for char in data[1:-1]:
        # print(f'Char: {char}')

        if char == '(':
            stack.append(current_room)  # remember this room, so we can return to it
        elif char == '|':
            current_room = stack[-1]  # retrieve previously stored room after a detour
        elif char == ')':
            current_room = stack.pop()  # retrieve and remove previously stored room after detours have been processed
        else:
            direction = DIRECTIONS[char]

            # set current room's door in the direction traveled
            current_room.doors[direction] = Tristate.yes
            # coordinates for the new room
            new_position = current_room.position + direction.value
            # check if a room at this location already exists
            existing = [room for room in rooms if room.position == new_position]
            if existing:  # room already exists
                current_room = existing[0]  # update current room
            else:
                # create a new room with 4 'maybe' doors
                current_room = Room(new_position, {d: Tristate.maybe for d in Direction})
                # set new room's door opposite the direction traveled
                current_room.doors[OPPOSITE[direction]] = Tristate.yes
                # add room to collection
                rooms.append(current_room)

        # print('\n'.join(''.join(char for char in row) for row in construct_maze(rooms, current_room.position)) + '\n' + '-' * 100)

        # set distance for current room
        distances[current_room.position] = min(
            distances[current_room.position],
            distances[previous_position] + 1
        ) if distances[current_room.position] else distances[previous_position] + 1

        previous_position = current_room.position  # remember this position

    # convert leftover 'maybe' doors to walls
    for room in rooms:
        for direction, door in room.doors.items():
            room.doors[direction] = Tristate.no if door == Tristate.maybe else door

    return rooms, distances


def construct_maze(rooms: list[Room], pos: Point = None) -> list[list[str]]:
    min_x, max_x = min(room.position.x for room in rooms), max(room.position.x for room in rooms)
    min_y, max_y = min(room.position.y for room in rooms), max(room.position.y for room in rooms)

    h_size = (max_x - min_x + 1) * 2 + 1
    v_size = (max_y - min_y + 1) * 2 + 1

    grid = [[EMPTY for c in range(h_size)] for r in range(v_size)]

    for room in rooms:
        grid_x = (room.position.x - min_x) * 2 + 1
        grid_y = v_size - 1 - ((room.position.y - min_y) * 2 + 1)

        # room contents
        if room.position == pos:
            grid[grid_y][grid_x] = POS
        else:
            grid[grid_y][grid_x] = CURRENT if room.position == Point(0, 0) else ROOM

        # corners
        grid[grid_y-1][grid_x-1] = WALL
        grid[grid_y-1][grid_x+1] = WALL
        grid[grid_y+1][grid_x-1] = WALL
        grid[grid_y+1][grid_x+1] = WALL

        # doors
        for direction, door in room.doors.items():
            grid[grid_y-direction.value.y][grid_x+direction.value.x] = DOORS[direction] if door == Tristate.yes else DOORS_TRI[door]

    return grid


test_data = '''
^WNE$
^ENWWW(NEEE|SSE(EE|N))$
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    print(data)

    rooms, distances = get_rooms(data)
    # pprint(rooms)
    # print('\n'.join(''.join(char for char in row) for row in construct_maze(rooms)))

    # pprint(distances)

    print(f'End result: {max(distances.values())}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[1])
    # for line in test_data:
    #     main(line)

    # using test_data ^WNE$:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using test_data ^ENWWW(NEEE|SSE(EE|N))$:
    #   End result: 10
    #   Finished 'main' in less than a millisecond
    # using test_data ^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$:
    #   End result: 18
    #   Finished 'main' in less than a millisecond
    # using test_data ^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$:
    #   End result: 23
    #   Finished 'main' in less than a millisecond
    # using test_data ^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$:
    #   End result: 31
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 4721
    #   Finished 'main' in 11 seconds

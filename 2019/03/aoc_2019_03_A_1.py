# aoc_2019_03_A_1.py - Day 3: Crossed Wires - part 1
# What is the Manhattan distance from the central port to the closest intersection?
# https://adventofcode.com/2019/day/3


from tools import time_it

from dataclasses import dataclass

from pprint import pprint


DATA_PATH = './input_2019_03'


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, factor: int):
        return Point(self.x * factor, self.y * factor)

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)


DIRECTIONS = {
    'U': Point(0, 1),
    'D': Point(0, -1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_wires(data_lines: list[str]) -> list[list[str]]:
    return [line.split(',') for line in data_lines]


test_data = '''
R8,U5,L5,D3
U7,R6,D4,L4
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    wires = get_wires(data_lines)
    # pprint(wires)

    # calculate the minimum and maximum horizontal and vertical coordinates
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for wire in wires:
        current = Point(0, 0)
        for instruction in wire:
            current += DIRECTIONS[instruction[0]] * int(instruction[1:])
            if current.x < min_x:
                min_x = current.x
            if current.x > max_x:
                max_x = current.x
            if current.y < min_y:
                min_y = current.y
            if current.y > max_y:
                max_y = current.y
    # print(min_x, max_x, min_y, max_y)

    # pre populate grid
    grid = [[0 for _ in range(min_x, max_x+1)] for _ in range(min_y, max_y+1)]
    # pprint(grid)

    # mark both wires onto the grid
    for w, wire in enumerate(wires, 1):
        current = Point(-min_x, -min_y)

        for instruction in wire:
            dir, num = DIRECTIONS[instruction[0]], int(instruction[1:])
            for step in range(num):
                current += dir
                if grid[current.y][current.x] == 0:  # not yet visited
                    grid[current.y][current.x] = w
                elif grid[current.y][current.x] == w:  # visited by same wire
                    continue
                elif grid[current.y][current.x] == 3:  # already crossed
                    continue
                else:  # visited by other wire, but not by current wire
                    grid[current.y][current.x] = 3
    # pprint(grid)

    # find all crossings (3) and remember their coordinates
    crossings = [
        Point(x+min_x, y+min_y)
        for y in range(len(grid)) for x in range(len(grid[0]))
        if grid[y][x] == 3
    ]
    print(crossings)

    # find the crossing with the lowest manhattan distance to the origin
    result = min(crossings, key=lambda c: c.manhattan).manhattan

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0:2])
    # main(test_data[2:4])
    # main(test_data[4:6])

    # using test_data 1:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 159
    #   Finished 'main' in 4 milliseconds
    # using test_data 3:
    #   End result: 135
    #   Finished 'main' in 3 milliseconds
    # using input data:
    #   End result: 8015
    #   Finished 'main' in 25 seconds

    # # calculate the minimum and maximum horizontal and vertical coordinates
    # # to get an idea of how big an array we'll need
    # wires = get_wires(load_data(DATA_PATH)[0:2])
    # for wire in wires:
    #     min_x, max_x, min_y, max_y = 0, 0, 0, 0
    #     current = Point(0, 0)
    #     for instruction in wire:
    #         current += DIRECTIONS[instruction[0]] * int(instruction[1:])
    #         if current.x < min_x:
    #             min_x = current.x
    #         if current.x > max_x:
    #             max_x = current.x
    #         if current.y < min_y:
    #             min_y = current.y
    #         if current.y > max_y:
    #             max_y = current.y
    #     print(min_x, max_x, min_y, max_y)
    #
    #     # wire 1: min_x, max_x, min_y, max_y = 0 18409 -6339 3539
    #     # wire 2: min_x, max_x, min_y, max_y = -6364 7655 -269 6059
    #     # min_x, max_x, min_y, max_y = -6364 18409 -6339 6059
    #     # x-range, y-range = 24774 12399
    #     # total cells needed in array: 307_172_826

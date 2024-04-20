# aoc_2019_03_A_2.py - Day 3: Crossed Wires - part 1
# What is the Manhattan distance from the central port to the closest intersection?
# https://adventofcode.com/2019/day/3
# in aoc_2019_03_A_1 I wanted to see if I could get away with creating an array of 24_774 * 12_399 = 307_172_826 units
# turns out I could, but I still wanted to try it the 'correct' way:
# in this version I will only keep track of the coordinates of the corners and calculate where the crossings are


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


def get_instructions(data_lines: list[str]) -> list[list[str]]:
    return [line.split(',') for line in data_lines]


def get_corners(instructions: list[str]) -> list[Point]:
    corners: list[Point] = []
    current = Point(0, 0)

    for instruction in instructions:
        corners.append(current)
        current += DIRECTIONS[instruction[0]] * int(instruction[1:])

    return corners + [current]


def find_crossings(wire_1: list[Point], wire_2: list[Point]) -> list[Point]:
    crossings: list[Point] = []

    for first_1, last_1 in zip(wire_1, wire_1[1:]):  # loop through all segments
        if first_1.x == last_1.x:  # vertical line
            # find all horizontal segments in wire_2 and see if they cross with the current segment
            y1, y2 = sorted((first_1.y, last_1.y))
            for first_2, last_2 in zip(wire_2, wire_2[1:]):  # loop through all segments
                if first_2.y == last_2.y:
                    if y1 <= first_2.y <= y2:
                        x1, x2 = sorted((first_2.x, last_2.x))
                        if x1 <= first_1.x <= x2:
                            crossings.append(Point(first_1.x, first_2.y))
        else:  # horizontal line
            # find all vertical segments in wire_2 and see if they cross with the current segment
            x1, x2 = sorted((first_1.x, last_1.x))
            for first_2, last_2 in zip(wire_2, wire_2[1:]):  # loop through all segments
                if first_2.x == last_2.x:
                    if x1 <= first_2.x <= x2:
                        y1, y2 = sorted((first_2.y, last_2.y))
                        if y1 <= first_1.y <= y2:
                            crossings.append(Point(first_2.x, first_1.y))

    return [crossing for crossing in crossings if crossing != Point(0, 0)]


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
    wires = get_instructions(data_lines)
    # pprint(wires)

    wire_1 = get_corners(wires[0])
    # pprint(wire_1)

    wire_2 = get_corners(wires[1])
    # pprint(wire_2)

    crossings = find_crossings(wire_1, wire_2)
    # pprint(crossings)

    print(f'End result: {min(crossings, key=lambda c: c.manhattan).manhattan}')


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
    #   Finished 'main' in less than a millisecond
    # using test_data 3:
    #   End result: 135
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 8015
    #   Finished 'main' in 7 milliseconds

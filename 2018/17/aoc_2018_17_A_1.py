# aoc_2018_17_A_1.py - Day 17: Reservoir Research - part 1
# How many tiles can the water reach within the range of y values in your scan?
# https://adventofcode.com/2018/day/17


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2018_17'

CLAY = '#'
SAND = '.'
SPRING = '+'
WATER = '~'


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _get_array(expression: str) -> list[int]:
    if '..' in expression:
        return list(range(int(expression.split('..')[0]), int(expression.split('..')[1])+1))
    else:
        return [int(expression)]


def get_clay(data_lines: list[str]) -> dict[Point, str]:
    squares = {}

    for line in data_lines:
        x_array = y_array = None

        left, right = line.split(', ')
        if left[0] == 'x':
            x_array = _get_array(left[2:])
            y_array = _get_array(right[2:])
        else:
            y_array = _get_array(left[2:])
            x_array = _get_array(right[2:])

        for y in y_array:
            for x in x_array:
                squares[Point(x, y)] = CLAY

    return squares


def draw_map(points: dict[Point, str]) -> None:
    min_x, max_x = min(p.x for p in points) - 1, max(p.x for p in points) + 1

    line = line = [SAND] * (max_x - min_x + 1)
    line[500 - min_x] = SPRING
    print(''.join(line))

    for y in range(min(p.y for p in points), max(p.y for p in points) + 1):
        line = [SAND] * (max_x - min_x + 1)
        for point in [s for s in points if s.y == y]:
            line[point.x - min_x] = points[point]
        print(''.join(line))

    line = [SAND] * (max_x - min_x + 1)
    print(''.join(line))


# test_data = '''
# x=1, y=1..3
# x=3, y=1..3
# y=4, x=1..3
# '''.strip().splitlines()

# test_data = '''
# x=0..5, y=0..5
# '''.strip().splitlines()

test_data = '''
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    points = get_clay(data_lines)
    # pprint(points)
    draw_map(points)

    # print(f'End result: {0}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using input data:
    #   End result: 34775
    #   Finished by manually adding characters in a text file

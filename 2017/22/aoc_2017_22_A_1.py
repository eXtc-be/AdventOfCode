# aoc_2017_22_A_1.py - Day 22: Sporifica Virus - part 1
# After 10_000 bursts of activity, how many bursts cause a node to become infected?
# https://adventofcode.com/2017/day/22


from tools import time_it

from dataclasses import dataclass

from pprint import pprint


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def distance(self, other: 'Point') -> int:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        return dx + max(0, (dy - dx) // 2)


DATA_PATH = './input_2017_22'

HEADINGS = {
    'N': {'L': 'W', 'R': 'E', 'friendly': 'north'},
    'E': {'L': 'N', 'R': 'S', 'friendly': 'east'},
    'S': {'L': 'E', 'R': 'W', 'friendly': 'south'},
    'W': {'L': 'S', 'R': 'N', 'friendly': 'west'},
}

DIRECTIONS = {
    'N': Point(0, 1),
    'E': Point(1, 0),
    'S': Point(0, -1),
    'W': Point(-1, 0),
}

INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'
CLEAN = '.'

ROUNDS = 10_000
ROUNDS_TEST = 70


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_infected(data_lines: list[str]) -> list[Point]:
    return [
        Point(x, -y)
        for y, line in enumerate(data_lines, -(len(data_lines)//2))
        for x, char in enumerate(line, -(len(line)//2))
        if char == INFECTED
    ]


new_infections = 0


def do_step(points: list[Point], location: Point, heading: str) -> tuple[Point, str]:
    global new_infections
    turn = None

    if location in points:
        turn = 'R'
        points.remove(location)
    else:
        turn = 'L'
        points.append(location)
        new_infections += 1

    new_heading = HEADINGS[heading][turn]
    new_location = location + DIRECTIONS[new_heading]

    return new_location, new_heading


def draw_grid(
        infected: list[Point],
        loc: Point = None,
        ul: Point = None,
        dr: Point = None,
        weakened: list[Point] = [],
        flagged: list[Point] = [],
) -> None:
    if not ul:
        min_x = min(point.x for point in infected)
        min_y = min(point.y for point in infected)
    else:
        min_x = ul.x
        min_y = ul.y
    if not dr:
        max_x = max(point.x for point in infected)
        max_y = max(point.y for point in infected)
    else:
        max_x = dr.x
        max_y = dr.y

    for y in range(max_y, min_y-1, -1):
        # print(''.join(INFECTED if Point(x, y) else CLEAN in points for x in range(max_x-1, min_x-1, -1)))
        for x in range(min_x, max_x+1):
            if Point(x, y) in infected:
                char = INFECTED
            elif Point(x, y) in weakened:
                char = WEAKENED
            elif Point(x, y) in flagged:
                char = FLAGGED
            else:
                char = CLEAN
            if Point(x, y) == loc:
                print(f'[{char}]', end='')
            else:
                print(f' {char} ', end='')
        print()


test_data = '''
..#
#..
...
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    global new_infections

    infected = get_infected(data_lines)
    # print(infected)

    location = Point(0, 0)
    heading = 'N'

    # print(location, heading, infected)
    # draw_grid(infected, location, Point(-15, -15), Point(15, 15))
    # print('-' * 100)

    for round in range(rounds):
        location, heading = do_step(infected, location, heading)
        # print(location, heading, infected)
        # draw_grid(infected, location, Point(-5, -5), Point(5, 5))
        # print('-' * 100)

    print(f'End result: {new_infections}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    # main(data_lines)
    main(data_lines, ROUNDS_TEST)
    # using test_data with 7 rounds:
    #   End result: 5
    #   Finished 'main' in less than a millisecond
    # using test_data with 70 rounds:
    #   End result: 70
    #   Finished 'main' in less than a millisecond
    # using test_data with 10000 rounds:
    #   End result: 5587
    #   Finished 'main' in 2.1 seconds
    # using input data:
    #   End result: 5280
    #   Finished 'main' in 1.98 seconds

    # # test draw_grid
    # points = get_infected(data_lines)
    # draw_grid(points)
    # draw_grid(points, Point(0, 0))
    # draw_grid(points, Point(0, 0), Point(-5, -5), Point(5, 5))

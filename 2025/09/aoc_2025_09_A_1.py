# aoc_2025_09_A_1.py - Day 9: Movie Theater - part 1
# Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?
# https://adventofcode.com/2025/day/9
from itertools import combinations

from tools import time_it

# other imports

from pprint import pprint
from collections import namedtuple


DATA_PATH = './input_2025_09'

# other constants


# classes
Point = namedtuple('Point', 'x y')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def get_points(lines: list[str]) -> list[Point]:
    return [Point(*[int(coord) for coord in line.split(',')]) for line in lines]


test_data = '''
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    points = get_points(data_lines)

    result = max(
        (abs(second.x - first.x) + 1) * (abs(second.y - first.y) + 1)
        for first, second in combinations(points, 2)
    )

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 50
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4771532800
    #   Finished 'main' in 38 milliseconds

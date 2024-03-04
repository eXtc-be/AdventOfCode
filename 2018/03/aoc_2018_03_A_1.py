# aoc_2018_03_A_1.py - Day 3: No Matter How You Slice It - part 1
# How many square inches of fabric are within two or more claims?
# https://adventofcode.com/2018/day/3


from tools import time_it

from dataclasses import dataclass
import re

from pprint import pprint


DATA_PATH = './input_2018_03'

CLAIM = re.compile(r'^\s*#(?P<id>\d+)\s+@\s+(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)\s*$')


@dataclass
class Claim:
    id: int
    x: int
    y: int
    w: int
    h: int


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_claims(data_lines: list[str]) -> list[Claim]:
    claims = []

    for line in data_lines:
        matches = CLAIM.match(line)
        if matches:
            claims.append(Claim(
                int(matches.group('id')),
                int(matches.group('x')),
                int(matches.group('y')),
                int(matches.group('w')),
                int(matches.group('h')),
            ))

    return claims


test_data = '''
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    claims = get_claims(data_lines)
    # pprint(claims)

    total_width = max(claim.x + claim.w for claim in claims)
    total_height = max(claim.y + claim.h for claim in claims)

    grid = [[0 for _ in range(total_width)] for _ in range(total_height)]
    # pprint(grid)

    for claim in claims:
        for y in range(claim.y, claim.y + claim.h):
            for x in range(claim.x, claim.x + claim.w):
                grid[y][x] += 1
    # pprint(grid)

    print(f'End result: {sum(sum(1 if cell > 1 else 0 for cell in row) for row in grid)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 111935
    #   Finished 'main' in 137 milliseconds

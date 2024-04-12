# aoc_2018_23_A_1.py - Day 23: Experimental Emergency Teleportation - part 1
# Find the nanobot with the largest signal radius. How many nanobots are in range of its signals?
# https://adventofcode.com/2018/day/23


from tools import time_it

from dataclasses import dataclass, field
import re

from pprint import pprint


DATA_PATH = './input_2018_23'

BOT = re.compile(r'pos=<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)>,\s+r=(?P<r>\d+)')


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __lt__(self, other: 'Point'):
        return self.distance(Point(0, 0, 0)) < other.distance(Point(0, 0, 0))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def distance(self, other: 'Point' = None):
        if other is None:
            # self.x - origin.x + self.y - origin.y + self.z - origin.z = self.x-0 + self.y-0 + self.z-0
            return self.x + self.y + self.z
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


@dataclass
class Bot:
    loc: Point
    r: int

    def distance(self, other: 'Bot' = None):
        if other is None:
            return self.loc.distance(None)
        return self.loc.distance(other.loc)

    def in_cube(self, p_1: Point, p_2: Point) -> bool:
        dist_squared = self.r ** 2

        if self.loc.x < p_1.x:
            dist_squared -= (self.loc.x - p_1.x) ** 2
        elif self.loc.x > p_2.x:
            dist_squared -= (self.loc.x - p_2.x) ** 2

        if self.loc.y < p_1.y:
            dist_squared -= (self.loc.y - p_1.y) ** 2
        elif self.loc.y > p_2.y:
            dist_squared -= (self.loc.y - p_2.y) ** 2

        if self.loc.z < p_1.z:
            dist_squared -= (self.loc.z - p_1.z) ** 2
        elif self.loc.z > p_2.z:
            dist_squared -= (self.loc.z - p_2.z) ** 2

        return dist_squared > 0

    def in_range(self, point: Point) -> bool:
        return point.distance(self.loc) <= self.r

def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_bots(data_lines: list[str], divisor: int = 1) -> list[Bot]:
    bots = []
    for line in data_lines:
        if match := BOT.match(line):
            bots.append(Bot(
                Point(
                    int(match.group('x')) // divisor,
                    int(match.group('y')) // divisor,
                    int(match.group('z')) // divisor
                ),
                int(match.group('r')) // divisor,
            ))
    return bots


test_data = '''
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    bots = get_bots(data_lines)
    # pprint(bots)

    strongest = max(bots, key=lambda b: b.r)
    # print(strongest)

    # in_range = []
    # for bot in bots:
    #     print(bot, d := bot.distance(strongest), end=' -> ')
    #     if d <= strongest.r:
    #         in_range.append(bot)
    #         print('in range')
    #     else:
    #         print('NOT in range')
    in_range = [bot for bot in bots if bot.distance(strongest) <= strongest.r]
    # pprint(in_range)

    print(f'End result: {len(in_range)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 7
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 399
    #   Finished 'main' in 3 milliseconds

# aoc_2018_25_A_1.py - Day 25: Four-Dimensional Adventure - part 1
# How many constellations are formed by the fixed points in spacetime?
# https://adventofcode.com/2018/day/25
# based on reddit user seligman99's solution (see extern_1.py)
# https://old.reddit.com/r/adventofcode/comments/a9c61w/2018_day_25_solutions/eci5k6c/
# I originally used lists to keep track of all the points, but when I ran the program, and it didn't
# finish for many minutes (the original did it in a couple of seconds), I replaced most of them with sets
# the program still takes almost 6 seconds, but at least it finishes in a reasonable time.
# the original program doesn't keep track of constellations (it only counts how many there are), and is
# a lot faster because of that. I just wanted something that could show the constellations.
# the overhead of using a class probably doesn't help either..


from tools import time_it

from dataclasses import dataclass
from collections import deque

from pprint import pprint


DATA_PATH = './input_2018_25'

DISTANCE = 3


@dataclass
class Point:
    x: int
    y: int
    z: int
    t: int

    def distance(self, other: 'Point' = None):
        if other is None:
            other = Point(0, 0, 0, 0)
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.t - other.t)

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.t))


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_points(data_lines: list[str]) -> list[Point]:
    return [Point(*map(int, line.split(','))) for line in data_lines]


def find_constellations(points: list[Point]) -> list[set[Point]]:
    constellations: list[set[Point]] = []
    used = set()

    while True:
        queue = deque()

        for point in points:
            if point not in used:
                queue.append(point)
                break

        constellation: set[Point] = set()

        while queue:
            current = queue.popleft()
            constellation.add(current)
            used.add(current)
            for point in points:
                if point not in used and point not in constellation:
                    if point.distance(current) <= DISTANCE:
                        queue.append(point)

        if not constellation:
            break

        constellations.append(constellation)

        print(len(points) - len(used))

    return constellations


test_data = [
'''
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
'''.strip().splitlines(),  # 2
'''
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
'''.strip().splitlines(),  # 2
'''
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
'''.strip().splitlines(),  # 4
'''
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
'''.strip().splitlines(),  # 3
'''
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
'''.strip().splitlines()  # 8
]


@time_it
def main(data_lines: list[str]) -> None:
    points = get_points(data_lines)
    # pprint(points)

    constellations = find_constellations(points)
    # pprint(constellations)

    print(f'End result: {len(constellations)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[3])
    # for test in test_data:
    #     main(test)

    # using test_data[0]:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using test_data[1]:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using test_data[2]:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using test_data[3]:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using test_data[4]:
    #   End result: 8
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 388
    #   Finished 'main' in 5.6 seconds

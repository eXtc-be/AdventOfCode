# aoc_2019_18_A_2.py - Day 18: Many-Worlds Interpretation - part 1
# How many steps is the shortest path that collects all the keys?
# https://adventofcode.com/2019/day/18
# this version precalculates the shortest path between all points of interest (start, keys, doors)
# then tries to find the optimal path using those points
# turns out this performs even worse: example 4 (test_data[3]) now takes 6 minutes instead of 1'22" and
# the actual puzzle now takes 24 minutes instead of 6!


from aoc_2019_18_A_1 import (
    DATA_PATH, START, WALL, EMPTY, KEYS, DOORS,
    Node,
    load_data,
    _update_keys,
    test_data,
)

from tools import time_it

from dataclasses import dataclass
from itertools import combinations
from sys import maxsize

from pprint import pprint


# other constants


@dataclass
class Point:
    row: int
    col: int

    def __hash__(self):
        return hash((self.row, self.col))


def find_distance(grid: list[str], start: Point, stop: Point) -> tuple[int, set[str]]:
    def get_neighbors(node: Point) -> list[Point]:
        """helper function that returns a list of neighbors for a given node"""
        return [
            Point(node.row + direction.row, node.col + direction.col)
            for direction in (Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1))
            if grid[node.row + direction.row][node.col + direction.col] != WALL
        ]

    open_list = {start}
    closed_list = set()
    distances = {start: 0}
    parents = {start: start}

    while open_list:
        n = None

        for v in open_list:
            if n is None or distances[v] < distances[n]:
                n = v

        if n is None:
            return maxsize, set()

        if n == stop:
            path = []
            steps = 0
            doors = set()

            while parents[n] != n:
                steps += 1
                if grid[n.row][n.col] in DOORS:
                    doors.add(grid[n.row][n.col])
                n = parents[n]

            return steps, doors

        for m in get_neighbors(n):
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                distances[m] = distances[n] + 1

        open_list.remove(n)
        closed_list.add(n)

    return maxsize, set()


def collect_keys(grid: list[str]) -> int | None:
    start_node = None
    keys = ''
    points = []

    # find all points of interest (start, keys, doors)
    for r, row in enumerate(grid[1:-1], 1):
        for c, char in enumerate(row[1:-1], 1):
            if char == START or char in KEYS:
                points.append(Point(r, c))

            if char == START:
                start_node = Node(r, c)
            elif char in KEYS:
                keys = _update_keys(keys, char)

    # find the shortest path between all points of interest
    print('precalculating paths')
    p_distances: dict[Point, dict[Point, tuple[int, set[str]]]] = {p: {} for p in points}
    for combo in combinations(points, 2):
        # print(f'{combo[0]} <-> {combo[1]}', end=': ')
        distance, doors = find_distance(grid, *combo)
        # print(distance, doors)
        p_distances[combo[0]][combo[1]] = distance, doors
        p_distances[combo[1]][combo[0]] = distance, doors

    open_list = {start_node}
    closed_list = set()
    distances = {start_node: 0}
    parents = {start_node: start_node}

    # use precalculated paths to find all keys
    print('finding keys')
    counter = 0
    while open_list:
        if counter % 1000 == 0:
            print(counter, len(open_list))
        counter += 1

        n = None

        for v in open_list:
            if n is None or distances[v] < distances[n]:
                n = v

        if n is None:
            return None

        if n.keys == keys:
            return distances[n]

        neighbors = []
        for neighbor, (distance, doors) in p_distances[Point(n.row, n.col)].items():
            if grid[neighbor.row][neighbor.col] in keys and all(door.lower() in n.keys for door in doors):
                neighbors.append((
                    Node(
                        neighbor.row,
                        neighbor.col,
                        _update_keys(n.keys, grid[neighbor.row][neighbor.col])
                    ),
                    distance
                ))

        for m, distance in neighbors:
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                distances[m] = distances[n] + distance
            else:
                if distances[m] > distances[n] + distance:
                    distances[m] = distances[n] + distance
                    parents[m] = n

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

        open_list.remove(n)
        closed_list.add(n)


@time_it
def main(data_lines: list[str]) -> None:
    steps = collect_keys(data_lines)
    # pprint(steps)

    print(f'End result: {steps}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])

    # using test_data 0:
    #   End result: 8
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 86
    #   Finished 'main' in 5 milliseconds
    # using test_data 2:
    #   End result: 132
    #   Finished 'main' in 8 milliseconds
    # using test_data 3:
    #   End result: 136
    #   Finished 'main' in 6 minutes and 0 seconds on work computer
    #   Finished 'main' in 3 minutes and 30 seconds on home computer
    # using test_data 4:
    #   End result: 81
    #   Finished 'main' in 30 milliseconds
    # using input data:
    #   End result: 5392
    #   Finished 'main' in 24 minutes and 11 seconds on work computer
    #   Finished 'main' in 13 minutes and 19 seconds on home computer

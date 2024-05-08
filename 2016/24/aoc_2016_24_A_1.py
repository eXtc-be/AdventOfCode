# aoc_2016_24_A_1.py - Day 24: Air Duct Spelunking - part 1
# Given your actual map, and starting from location 0,
# what is the fewest number of steps required to visit every non-0 number marked on the map at least once?
# https://adventofcode.com/2016/day/24


from tools import time_it

from typing import NamedTuple
import re
from itertools import permutations, combinations
from sys import maxsize

from pprint import pprint


DATA_PATH = './input_2016_24'

NODE = re.compile(r'\d')

WALL = '#'
OPEN = '.'


class Point(NamedTuple):
    x: int
    y: int


class Node(NamedTuple):
    num: int
    loc: Point


class Pair(NamedTuple):
    nodes: list[Node]
    path: list[Point]


DIRECTIONS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def print_grid(grid: list[str], path: list[Point] = None) -> None:
    print('  ' + ''.join([str(i)[-1] for i in range(len(grid[0]))]))  # header
    for row in range(len(grid)):
        print(str(row)[-1], end=' ')
        for col in range(len(grid[row])):
            if path is not None and Point(col, row) in path:
                if grid[row][col] != WALL:
                    if Point(col, row) == path[0]:  # src
                        print('S', end='')
                    elif Point(col, row) == path[-1]:  # dst
                        print('D', end='')
                    else:  # path
                        print('O', end='')
                else:
                    print('X', end='')
            else:
                print(grid[row][col], end='')
        print(' ' + str(row)[-1])
    print('  ' + ''.join([str(i)[-1] for i in range(len(grid[0]))]))  # header


def get_nodes(grid: list[str]) -> list[Node]:
    nodes = []
    for r, row in enumerate(grid):
        for match in NODE.finditer(row):
            nodes.append(Node(
                int(match.group()),
                Point(
                    match.start(),
                    r
                )
            ))

    return nodes


def find_sub_path(grid: list[str], start_node: Point, stop_node: Point) -> list[Point] | None:
    """finds the optimal path between 2 nodes on the grid using A* algorithm"""
    def heuristic(node: Point) -> int:  # return Manhattan distance between node and stop_node
        return abs(node.x - stop_node.x) + abs(node.y - stop_node.y)

    def get_neighbors(node: Point) -> list[tuple[Point, int]]:
        return [
            (Point(node.x + direction.x, node.y + direction.y), 1)
            for direction in DIRECTIONS
            if 0 <= node.y + direction.y < len(grid) and
               0 <= node.x + direction.x < len(grid[node.y + direction.y]) and
               grid[node.y + direction.y][node.x + direction.x] != WALL
        ]

    open_list = {start_node}
    closed_list = set([])
    distances = {start_node: 0}
    parents = {start_node: start_node}

    while open_list:
        n = None

        # find a node with the lowest value of f() - evaluation function
        for v in open_list:
            if n is None or distances[v] + heuristic(v) < distances[n] + heuristic(n):
                n = v

        if n is None:
            # print('Path does not exist!')
            return None

        # if the current node is the stop_node
        # then we begin reconstructing the path from it to the start_node
        if n == stop_node:
            reconst_path = []

            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]

            reconst_path.append(start_node)

            reconst_path.reverse()

            # print('Path found: {}'.format(reconst_path))
            return reconst_path

        # for all neighbors of the current node do
        for (m, weight) in get_neighbors(n):
            # if the current node isn't in both open_list and closed_list
            # add it to open_list and note n as its parent
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                distances[m] = distances[n] + weight

            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update parent data and g data
            # and if the node was in the closed_list, move it to open_list
            else:
                if distances[m] > distances[n] + weight:
                    distances[m] = distances[n] + weight
                    parents[m] = n

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

        # remove n from the open_list, and add it to closed_list
        # because all of his neighbors were inspected
        open_list.remove(n)
        closed_list.add(n)

    # print('Path does not exist!')
    return None


def find_path(pairs: dict[int, dict[int, int]], loop_back: bool = False) -> list[tuple[list[int], int]]:
    """returns all possible paths that start at node 0 and go through all other nodes at least once
       by looping through all permutations of pairs (except the first one) """
    paths = []
    end_node = [0] if loop_back else []

    for perm in [[0]+list(p)+end_node for p in permutations(sorted(pairs.keys())[1:])]:
        paths.append((list(perm), sum(pairs[s][d] for s, d in zip(perm, perm[1:]))))

    return paths


test_data = '''
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
'''.strip().splitlines()


@time_it
def main(grid: list[str]) -> None:
    # print_grid(grid)

    nodes = get_nodes(grid)
    # print(sorted(nodes))

    # find the shortest path from any node to any other node
    pairs = {s.num: {d.num: 0 for d in nodes} for s in nodes}  # initialize dict of dicts
    for pair in combinations(nodes, 2):
        path = find_sub_path(grid, *[node.loc for node in pair])
        # print_grid(grid, path)
        pairs[pair[0].num][pair[1].num] = len(path)-1
        pairs[pair[1].num][pair[0].num] = len(path)-1
    # pprint(pairs)

    paths = find_path(pairs)
    # print(paths)

    shortest = sorted(paths, key=lambda p: p[1])[0]
    # print(shortest)

    print(f'End result: {shortest[1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 14
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 498
    #   Finished 'main' in 1.21 seconds

# aoc_2016_13_B_2.py - Day 13: A Maze of Twisty Little Cubicles - part 2
# How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?
# Solution 2: using Dijkstra's algorithm to find all distances - should be much faster
# https://adventofcode.com/2016/day/13


from aoc_2016_13_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    OPEN,
    Point,
    build_maze,
    find_path,
    print_maze,
)

from tools import time_it

from sys import maxsize

from pprint import pprint


DIRECTIONS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]


def manhattan(start_node: Point, stop_node: Point) -> int:  # return Manhattan distance between start_node and stop_node
    return abs(start_node.x - stop_node.x) + abs(start_node.y - stop_node.y)


def dijkstra(maze: list[list[str]], start_node: Point, reach: int) -> list[tuple[Point, int]]:
    # distances = [maxsize for _ in range(len(maze[0])) for _ in range(len(maze))]
    # distances[start_node.y * len(maze[0]) + start_node.x] = 0
    # processed = [False for _ in range(len(maze[0])) for _ in range(len(maze))]

    def get_neighbors(node: Point) -> list[Point]:
        """helper function that returns a list of neighbors for a given node"""
        return [
            Point(node.x + direction.x, node.y + direction.y)
            for direction in DIRECTIONS
            if 0 <= node.y + direction.y < len(maze) and
               0 <= node.x + direction.x < len(maze[node.y + direction.y]) and
               maze[node.y + direction.y][node.x + direction.x] == OPEN and
               manhattan(start_node, Point(node.x + direction.x, node.y + direction.y)) <= reach
        ]

    # keep track of each point's distance to the start node
    distances = {
        Point(c, r): maxsize
        for r in range(len(maze))
        for c in range(len(maze[0]))
        if manhattan(start_node, Point(c, r)) <= reach
    }
    # keep track whether each point has been fully processed
    processed = {
        Point(c, r): False
        for r in range(len(maze))
        for c in range(len(maze[0]))
        if manhattan(start_node, Point(c, r)) <= reach
    }

    distances[start_node] = 0  # set the distance for the start node

    # for _ in range(len(maze)*len(maze[0])):
    while not all(processed.values()):
        dist, u = min((d, p) for p, d in distances.items() if not processed[p])
        processed[u] = True

        for v in get_neighbors(u):
            if (
                maze[v.y][v.x] == OPEN and
                not processed[v] and
                distances[v] > dist + 1
            ):
                distances[v] = dist + 1

    return [(point, distance) for point, distance in distances.items() if distance <= reach]


test_maze = """
.#.##
..#..
#....
###.#
""".strip().splitlines()


@time_it
def main(maze: list[list[str]], start: Point, reach: int) -> None:
    reachable = dijkstra(maze, start, reach)
    # pprint(reachable)

    print(f'End result: {len(reachable)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    start = Point(1, 1)  # both
    end = Point(31, 39)  # real
    # end = Point(7, 4)  # test
    reach = 50  # real
    # reach = 5  # test

    maze = build_maze(end.y * 2, end.x * 2, int(data_lines[0]))
    # maze = [[c for c in line] for line in test_maze]
    # print_maze(maze)

    main(maze, start, reach)
    # using test_data:
    #   End result: 11
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 127
    #   Finished 'main' in 294 milliseconds

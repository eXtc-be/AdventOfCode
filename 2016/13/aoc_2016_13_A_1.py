# aoc_2016_13_A_1.py - Day 13: A Maze of Twisty Little Cubicles - part 1
# What is the fewest number of steps required for you to reach 31,39?
# https://adventofcode.com/2016/day/13


from tools import time_it

from typing import NamedTuple

from pprint import pprint

DATA_PATH = './input_2016_13'

WALL = '#'
OPEN = '.'


class Point(NamedTuple):
    x: int
    y: int


DIRECTIONS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def print_maze(maze: list[list[str]], path: list[Point] = None) -> None:
    print('  ' + ''.join([str(i)[-1] for i in range(len(maze[0]))]))  # header
    for row in range(len(maze)):
        print(str(row)[-1], end=' ')
        for col in range(len(maze[row])):
            if path is not None and Point(col, row) in path:
                if maze[row][col] == OPEN:
                    if Point(col, row) == path[0]:  # src
                        print('S', end='')
                    elif Point(col, row) == path[-1]:  # dst
                        print('D', end='')
                    else:  # path
                        print('O', end='')
                else:
                    print('X', end='')
            else:
                print(maze[row][col], end='')
        print(' ' + str(row)[-1])
    print('  ' + ''.join([str(i)[-1] for i in range(len(maze[0]))]))  # header


def _compute_wall(x: int, y: int, fav: int) -> bool:
    number = x * x + 3 * x + 2 * x * y + y + y * y + fav
    binary = f'{number:b}'
    return binary.count('1') % 2 == 1


def build_maze(rows: int, cols: int, fav: int) -> list[list[str]]:
    maze = [[OPEN for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if _compute_wall(col, row, fav):
                maze[row][col] = WALL

    return maze


def find_path(maze: list[list[str]], start_node: Point, stop_node: Point) -> list[Point] | None:
    def heuristic(node: Point) -> int:  # return Manhattan distance between node and stop_node
        return abs(node.x - stop_node.x) + abs(node.y - stop_node.y)

    def get_neighbors(node: Point) -> list[tuple[Point, int]]:
        return [
            (Point(node.x + direction.x, node.y + direction.y), 1)
            for direction in DIRECTIONS
            if 0 <= node.y + direction.y < len(maze) and
               0 <= node.x + direction.x < len(maze[node.y + direction.y]) and
               maze[node.y + direction.y][node.x + direction.x] == OPEN
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


test_data = '''
10
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], start: Point, end: Point) -> None:
    maze = maze = build_maze(end.y * 2, end.x * 2, int(data_lines[0]))
    # print_maze(maze)

    path = find_path(maze, start, end)
    # print_maze(maze, path)

    print(f'End result: {len(path) - 1}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    start = Point(1, 1)
    end = Point(31, 39)  # real
    # end = Point(7, 4)  # test

    main(data_lines, start, end)
    # using test_data:
    #   End result: 11
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 86
    #   Finished 'main' in 5 milliseconds

    # # test build_maze / print_maze
    # maze = build_maze(7, 10, int(data_lines[0]))
    # # maze = build_maze(end.y * 2, end.x * 2, int(data_lines[0]))
    # path = [
    #     Point(1, 1),
    #     Point(1, 2),
    #     Point(2, 2),
    #     Point(3, 2),
    #     Point(3, 3),
    #     Point(3, 4),
    #     Point(4, 4),
    #     Point(4, 5),
    #     Point(5, 5),
    #     Point(6, 5),
    #     Point(6, 4),
    #     Point(7, 4),
    # ]
    # # path = [
    # #     Point(1, 1),
    # #     Point(7, 4),
    # # ]
    # # print_maze(maze, path)
    # print_maze(maze, path)

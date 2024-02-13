# aoc_2016_13_B_1.py - Day 13: A Maze of Twisty Little Cubicles - part 2
# How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?
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

# other imports

from pprint import pprint


# other constants


def Manhattan(start_node: Point, stop_node: Point) -> int:  # return Manhattan distance between start_node and stop_node
    return abs(start_node.x - stop_node.x) + abs(start_node.y - stop_node.y)


@time_it
def main(data_lines: list[str], start: Point, end: Point, reach: int) -> None:
    maze = maze = build_maze(end.y * 2, end.x * 2, int(data_lines[0]))
    # print_maze(maze)

    reachable = []

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            stop = Point(col, row)
            if maze[row][col] == OPEN and Manhattan(start, stop) <= reach:
                path = find_path(maze, start, stop)
                if path is not None and len(path)-1 <= reach:
                    reachable.append((stop, path))

    # pprint(reachable)
    # print_maze(maze, [t[0] for t in reachable])

    print(f'End result: {len(reachable)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    start = Point(1, 1)
    end = Point(31, 39)  # real
    # end = Point(7, 4)  # test
    reach = 50  # real
    # reach = 5  # test

    main(data_lines, start, end, reach)
    # using test_data:
    #   End result: 11
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 127
    #   Finished 'main' in 1.88 seconds

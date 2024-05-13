# aoc_2019_18_A_1.py - Day 18: Many-Worlds Interpretation - part 1
# How many steps is the shortest path that collects all the keys?
# https://adventofcode.com/2019/day/18
# finds the correct solution for all examples and the actual data using A*
# it is very slow, probably because many paths are re-calculated many times


from tools import time_it

import string
from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2019_18'

START = '@'
WALL = '#'
EMPTY = '.'
KEYS = string.ascii_lowercase
DOORS = string.ascii_uppercase


@dataclass
class Node:
    row: int
    col: int
    keys: str = ''

    def __hash__(self):
        return hash((self.row, self.col, self.keys))


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _update_keys(keys: str, new: str) -> str:
    # print(keys, new)
    return ''.join(sorted(set(list(keys) + [new])))


def _get_neighbors(grid: list[str], node: Node) -> list[Node]:
    neighbors = []

    for direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        # no need to do boundary checks, because all the edges are walls
        neighbor = grid[node.row + direction[0]][node.col + direction[1]]
        if neighbor == EMPTY or neighbor == START:
            neighbors.append(Node(node.row + direction[0], node.col + direction[1], node.keys))
        elif neighbor in KEYS:
            neighbors.append(Node(node.row + direction[0], node.col + direction[1], _update_keys(node.keys, neighbor)))
        elif neighbor in DOORS:
            if neighbor.lower() in node.keys:
                neighbors.append(Node(node.row + direction[0], node.col + direction[1], node.keys))

    return neighbors


def collect_keys(grid: list[str]) -> list[Node] | None:
    start_node = None
    keys = ''

    # find all keys and the start position
    for r, row in enumerate(grid[1:-1], 1):
        for c, char in enumerate(row[1:-1], 1):
            if char == START:
                start_node = Node(r, c)
            elif char in KEYS:
                keys = _update_keys(keys, char)

    open_list = {start_node}
    closed_list = set()
    distances = {start_node: 0}
    parents = {start_node: start_node}

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
            path = []

            while parents[n] != n:
                path.append(n)
                n = parents[n]

            path.append(start_node)

            path.reverse()

            return path

        for m in _get_neighbors(grid, n):
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                distances[m] = distances[n] + 1  # weight for this kind of grid is always 1

        open_list.remove(n)
        closed_list.add(n)


test_data = [
'''
#########
#b.A.@.a#
#########
'''.strip().splitlines(),
'''
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
'''.strip().splitlines(),
'''
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
'''.strip().splitlines(),
'''
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
'''.strip().splitlines(),
'''
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
'''.strip().splitlines(),
]


@time_it
def main(data_lines: list[str]) -> None:
    steps = collect_keys(data_lines)
    # pprint(steps)

    print(f'End result: {len(steps) - 1}')


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
    #   Finished 'main' in 2 milliseconds
    # using test_data 2:
    #   End result: 132
    #   Finished 'main' in 3 milliseconds
    # using test_data 3:
    #   End result: 136
    #   Finished 'main' in 1 minute and 22 seconds on work computer
    #   Finished 'main' in 59 seconds on home computer
    # using test_data 4:
    #   End result: 81
    #   Finished 'main' in 14 milliseconds
    # using input data:
    #   End result: 5392
    #   Finished 'main' in 6 minutes and 15 seconds on work computer
    #   Finished 'main' in 4 minutes and 16 seconds on home computer

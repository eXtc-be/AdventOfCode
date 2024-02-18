# aoc_2016_22_B_1.py - Day 22: Grid Computing - part 2
# How many viable pairs of nodes are there?
# https://adventofcode.com/2016/day/22


from aoc_2016_22_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    Node,
    get_nodes,
    find_viable_pairs,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def print_grid(nodes: list[Node], mode: str = 'numbers') -> None:
    nodes.sort(key=lambda n: (n.location.y, n.location.x))  # sort nodes by row, then column

    hole, walls = None, []
    if mode == 'symbols':
        hole = [node for node in nodes if node.used == 0][0]
        walls = [node for node in nodes if node.used > hole.free]

    max_x = max(node.location.x for node in nodes)

    current_row = nodes[0].location.y
    for node in nodes:
        if node.location.y > current_row:
            print()
            current_row = node.location.y
        if mode == 'numbers':
            print(f'{node.used:3}/{node.free:3}', end=' ')
        elif mode == 'symbols':
            if node.location.x == 0 and node.location.y == 0:  # source node
                print('(.)', end=' ')
            elif node.location.x == max_x and node.location.y == 0:  # destination node
                print(' G ', end=' ')
            elif node in walls:
                print(' # ', end=' ')
            elif node == hole:
                print(' _ ', end=' ')
            else:
                print(' . ', end=' ')
    print()


test_data = '''
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # pprint(nodes)
    # print_grid(nodes)
    print_grid(nodes, 'symbols')

    # pairs = find_viable_pairs(nodes)
    # pprint(pairs)

    # print(f'End result: {0}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 218
    #   Finished by hand

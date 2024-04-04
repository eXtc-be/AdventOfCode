# aoc_2016_22_A_1.py - Day 22: Grid Computing - part 1
# How many viable pairs of nodes are there?
# https://adventofcode.com/2016/day/22


from tools import time_it

from dataclasses import dataclass, field
from itertools import permutations

from pprint import pprint


DATA_PATH = './input_2016_22'

# other constants


@dataclass
class Point:
    x: int
    y: int



@dataclass
class Node:
    location: Point
    size: int
    used: int
    free: int
    pct: int



def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_nodes(datalines: list[str]) -> list[Node]:
    nodes = []

    for line in datalines:
        if '/' in line:
            name, size, used, avail, pct = line.split()
            x, y = name.split('-')[-2:]
            nodes.append(Node(
                Point(int(x[1:]), int(y[1:])),
                int(size[:-1]),
                int(used[:-1]),
                int(avail[:-1]),
                int(pct[:-1]),
            ))

    return nodes


def find_viable_pairs(nodes: list[Node]) -> list[tuple[Node, Node]]:
    pairs = []

    for node_a, node_b in permutations(nodes, 2):
        if 0 < node_a.used <= node_b.free:
            pairs.append((node_a, node_b))

    return pairs


test_data = '''
root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     94T   72T    22T   76%
/dev/grid/node-x0-y1     88T   73T    15T   82%
/dev/grid/node-x0-y2     88T   65T    23T   73%
/dev/grid/node-x0-y3     85T   72T    13T   84%
/dev/grid/node-x0-y4     91T   68T    23T   74%
/dev/grid/node-x3-y26    87T   64T    23T   73%
/dev/grid/node-x3-y27    85T   72T    13T   84%
/dev/grid/node-x3-y28    88T    0T    88T    0%
/dev/grid/node-x3-y29    90T   71T    19T   78%
/dev/grid/node-x3-y30    87T   73T    14T   83%
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # pprint(nodes)

    pairs = find_viable_pairs(nodes)
    # pprint(pairs)

    print(f'End result: {len(pairs)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 9
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 990
    #   Finished 'main' in 68 milliseconds

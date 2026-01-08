# aoc_2024_08_A_2.py - Day 8: Resonant Collinearity - part 1
# Calculate the impact of the signal. How many unique locations within the
# bounds of the map contain an antinode?
# https://adventofcode.com/2024/day/8

# improved implementation: instead of combining every node with every other node,
# we now combine only nodes with the same frequency


from tools import time_it

from aoc_2024_08_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_nodes,
)

# other imports

from pprint import pprint
from itertools import permutations


# other constants

EMPTY = '.'


# other functions

@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # print(nodes)

    max_x = len(data_lines[0]) - 1
    max_y = len(data_lines) - 1

    antinodes = set()
    for freq in set(node.freq for node in nodes):
        for node1, node2 in permutations([node for node in nodes if node.freq == freq], 2):
            # print(node1, node2, end=' -> ')
            antinode = node1.pos + (node1.pos - node2.pos)
            # print(antinode, end=' -> ')
            if 0 <= antinode.x <= max_x and 0 <= antinode.y <= max_y:
                antinodes.add(antinode)
                # print('added')
            else:
                # print('rejected')
                pass

    # print(antinodes)

    print(f'End result: {len(antinodes)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 14
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 305
    #   Finished 'main' in 1 millisecond

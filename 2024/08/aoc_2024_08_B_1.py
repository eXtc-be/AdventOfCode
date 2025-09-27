# aoc_2024_08_B_1.py - Day 8: Resonant Collinearity - part 2
# Calculate the impact of the signal using this updated model. How many
# unique locations within the bounds of the map contain an antinode?
# https://adventofcode.com/2024/day/8


from aoc_2024_08_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_nodes,
)

from tools import time_it

# other imports

from pprint import pprint
from itertools import permutations


# other constants


# other functions


# test_data = '''
# T.........
# ...T......
# .T........
# ..........
# ..........
# ..........
# ..........
# ..........
# ..........
# ..........
# '''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # print(nodes)

    max_x = len(data_lines[0]) - 1
    max_y = len(data_lines) - 1

    antinodes = set()
    for freq in set(node.freq for node in nodes):
        for node1, node2 in permutations([node for node in nodes if node.freq == freq], 2):
            factor = 0
            while True:
                # print(node1, node2, factor, end=' -> ')
                antinode = node1.pos + factor * (node1.pos - node2.pos)
                # print(antinode, end=' -> ')
                if 0 <= antinode.x <= max_x and 0 <= antinode.y <= max_y:
                    antinodes.add(antinode)
                    # print('added')
                    factor += 1
                else:
                    # print('rejected')
                    break

    # print(antinodes)

    print(f'End result: {len(antinodes)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 34
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1150
    #   Finished 'main' in 4 milliseconds

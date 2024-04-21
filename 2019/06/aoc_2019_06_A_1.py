# aoc_2019_06_A_1.py - Day 6: Universal Orbit Map - part 1
# What is the total number of direct and indirect orbits in your map data?
# https://adventofcode.com/2019/day/6


from tools import time_it

from collections import defaultdict

from pprint import pprint


DATA_PATH = './input_2019_06'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_nodes(data_lines: list[str]) -> dict[str, list[str]]:
    nodes = defaultdict(list)

    for line in data_lines:
        parent, child = line.split(')')
        nodes[parent].append(child)

    return nodes


def calc_orbits(nodes: dict[str, list[str]], root: str, prev: int = 0) -> int:
    total = 0

    if root in nodes:
        for child in nodes[root]:
            total += 1 + prev + calc_orbits(nodes, child, prev + 1)

    return total


# test_data = '''
# COM)A
# COM)B
# A)C
# A)D
# B)E
# B)F
# C)G
# G)H
# '''.strip().splitlines()

test_data = '''
B)C
G)H
K)L
C)D
E)J
J)K
E)F
B)G
D)E
D)I
COM)B
'''.strip().splitlines()

# test_data = '''
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# '''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # pprint(nodes)

    orbits = calc_orbits(nodes, 'COM')
    # print(orbits)

    print(f'End result: {orbits}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 42
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 312697
    #   Finished 'main' in 2 milliseconds

# aoc_2019_06_B_1.py - Day 6: Universal Orbit Map - part 2
# What is the total number of direct and indirect orbits in your map data?
# https://adventofcode.com/2019/day/6


from aoc_2019_06_A_1 import (
    DATA_PATH,
    load_data,
    get_nodes,
    # test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def find_path_to_origin(nodes: dict[str, list[str]], node: str) -> list[str]:
    path = []
    current = node

    while current != 'COM':
        for node, children in nodes.items():
            if current in children:
                current = node
                path.append(current)
                break

    return path


test_data = '''
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # pprint(nodes)

    path_you = find_path_to_origin(nodes, 'YOU')
    # print(path_you)
    path_san = find_path_to_origin(nodes, 'SAN')
    # print(path_san)

    common = None
    for node in path_you[1:-1]:
        if node in path_san:
            common = node
            break

    print(f'End result: {path_you.index(common) + path_san.index(common)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 466
    #   Finished 'main' in 30 milliseconds

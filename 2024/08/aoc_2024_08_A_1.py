# aoc_2024_08_A_1.py - Day 8: Resonant Collinearity - part 1
# Calculate the impact of the signal. How many unique locations within the
# bounds of the map contain an antinode?
# https://adventofcode.com/2024/day/8

# naive implementation: every node is combined with every other node
#   a lot of combinations are rejected because the frequencies don't match
#   this can be improved by considering only permutations of nodes with the same frequency


from tools import time_it

# other imports

from pprint import pprint
from dataclasses import dataclass, field
from itertools import permutations


DATA_PATH = './input_2024_08'

@dataclass
class Coord:
    x: int = 0
    y: int = 0

    # def distance(self, other: 'Coord' = None) -> int:
    #     other = Coord(0, 0) if other is None else other
    #     return abs(self.x - other.x) + abs(self.y - other.y)
    #
    def __add__(self, other: 'Coord'):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord'):
        return Coord(self.x - other.x, self.y - other.y)

    def __rmul__(self, other: int):
        return Coord(self.x * other, self.y * other)

    # def __str__(self):
    #     return f'({self.x}, {self.y})'
    #
    def __hash__(self):
        return hash((self.x, self.y))


@dataclass()
class Node:
    pos: Coord
    freq: str

    def __hash__(self):
        return hash((self.pos, self.freq))


# other constants

EMPTY = '.'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def get_nodes(data_lines: list[str]) -> list[Node]:
    nodes = []
    for y, line in enumerate(data_lines):
        for x, char in enumerate(line):
            if char != EMPTY:
                nodes.append(Node(Coord(x, y), char))
    return nodes


test_data = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nodes = get_nodes(data_lines)
    # print(nodes)

    max_x = len(data_lines[0]) - 1
    max_y = len(data_lines) - 1

    antinodes = set()
    for node1, node2 in permutations(nodes, 2):
        # print(node1, node2, end=' -> ')
        if node1.freq == node2.freq:
            antinode = node1.pos + (node1.pos - node2.pos)
            # print(antinode, end=' -> ')
            if 0 <= antinode.x <= max_x and 0 <= antinode.y <= max_y:
                antinodes.add(antinode)
                # print('added')
            else:
                # print('rejected')
                pass
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
    #   Finished 'main' in 3 milliseconds

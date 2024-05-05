# aoc_2023_11_A_1.py - Day 11: Cosmic Expansion - part 1
# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
# https://adventofcode.com/2023/day/11
# version 1: keep the entire universe in a 2D array


from tools import time_it

from itertools import combinations

from pprint import pprint


DATA_PATH = './input_2023_11'

EMPTY_SPACE = '.'
GALAXY = '#'
PATH = 'o'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_universe(data_lines: list[str]) -> list[list[str]]:
    """returns a 2-dimensional list containing the galaxies in the universe"""
    return [[char for char in line] for line in data_lines]


def expand_universe(universe: list[list[str]]) -> list[list[str]]:
    """finds empty rows and columns in the universe and expands them"""
    expanded_universe = []

    # double empty rows
    for row in universe:
        if row.count(GALAXY) == 0:
            expanded_universe.append(list(row))
        expanded_universe.append(list(row))

    # double empty columns
    for col in range(len(universe[0]) -1, -1, -1):  # right to left
        if sum(row[col] == GALAXY for row in universe) == 0:  # abuses the fact that True == 1 to get number of galaxies
            for row in expanded_universe:
                row.insert(col, EMPTY_SPACE)

    return expanded_universe


def get_galaxy_coords(universe: list[list[str]]) -> list[tuple[int, int]]:
    """finds the coordinates of all galaxies in the universe"""
    return [(r, c) for r, row in enumerate(universe) for c, cell in enumerate(row) if cell == GALAXY]


def shortest_path(first: tuple[int, int], second: tuple[int, int]) -> list[tuple[int, int]]:
    """finds the shortest path between 2 galaxies in the universe
    returns a list of coordinates for each cell between first and second"""

    # special case: horizontal line
    if (second[1] - first[1]) == 0:
        return [(x, first[1]) for x in range(min(first[0], second[0]), max(first[0], second[0]) + 1)]

    # special case: vertical line
    if (second[0] - first[0]) == 0:
        return [(first[0], y) for y in range(min(first[1], second[1]), max(first[1], second[1]) + 1)]

    # calculate slope m and offset q for line with formula y = mx + q
    m = (second[1] - first[1]) / (second[0] - first[0])
    q = first[1] - m * first[0]

    new_coords = []

    if abs(m) < 1:  # more horizontal - loop over x and calculate y
        coords = [(x, round(m * x + q)) for x in range(min(first[0], second[0]), max(first[0], second[0]) + 1)]
        # create an extra step where both coordinates jump at the same time
        for pair in zip(coords, coords[1:]):
            new_coords.append(pair[0])  # add the first coord of the pair
            if abs(pair[0][0] - pair[1][0]) > 0 and abs(pair[0][1] - pair[1][1]):
                new_coords.append((pair[1][0], pair[0][1]))  # add intermediate coord
        new_coords.append(coords[-1])  # add the final coord
    else:  # more vertical - loop over y and calculate x
        coords = [(round((y - q) / m), y) for y in range(min(first[1], second[1]), max(first[1], second[1]) + 1)]
        # create an extra step where both coordinates jump at the same time
        for pair in zip(coords, coords[1:]):
            new_coords.append(pair[0])  # add the first coord of the pair
            if abs(pair[0][0] - pair[1][0]) > 0 and abs(pair[0][1] - pair[1][1]):
                new_coords.append((pair[0][0], pair[1][1]))  # add intermediate coord
        new_coords.append(coords[-1])  # add the final coord

    return new_coords


def draw_universe(universe: list[list[str]]) -> None:
    """draws the universe"""
    for row in universe:
        print(''.join(row))
    print('-' * 100)


test_data = '''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    universe = create_universe(data_lines)
    # draw_universe(universe)

    expanded_universe = expand_universe(universe)
    # draw_universe(expanded_universe)

    coords = get_galaxy_coords(expanded_universe)
    # print(coords)

    path_lengths = []
    for pair in combinations(coords, 2):
        # test_universe = [[cell for cell in row] for row in expanded_universe]
        # draw_universe(test_universe)
        path = shortest_path(*pair)
        # print(pair, len(path) - 1)
        # print(pair, path, len(path) - 1)
        path_lengths.append(len(path) - 1)
        # for coord in path:
        #     test_universe[coord[0]][coord[1]] = PATH
        # draw_universe(test_universe)

    print(f'End result: {sum(path_lengths)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 374
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 9947476
    #   Finished 'main' in 3.4 seconds

    # # test shortest_path
    # test_universe = [['.' for _ in range(10)] for _ in range(10)]
    # draw_universe(test_universe)
    # for test in (
    #         ((1, 1), (8, 8)),  # m=1
    #         ((1, 8), (8, 1)),  # m=-1
    #         ((1, 1), (1, 8)),  # vertical
    #         ((1, 1), (8, 1)),  # horizontal
    #         ((2, 1), (8, 4)),  # m=1/2
    #         ((2, 4), (8, 1)),  # m=-1/2
    #         ((1, 2), (4, 8)),  # m=2
    # ):
    #     path = shortest_path(*test)
    #     print(test, path)
    #     test_universe = [['.' for _ in range(10)] for _ in range(10)]
    #     for coord in path:
    #         test_universe[coord[0]][coord[1]] = PATH
    #     draw_universe(test_universe)

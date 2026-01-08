# aoc_2023_11_A_2.py - Day 11: Cosmic Expansion - part 1
# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
# https://adventofcode.com/2023/day/11
# version 2: use coordinates for galaxies instead of storing the whole universe in a 2D array,
# shortest_path just returns the number of steps instead of all the steps
# (for the special cases horizontal and vertical, the code is already optimized
# by returning the difference between coordinates)


from aoc_2023_11_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    EMPTY_SPACE,
    GALAXY,
)

from tools import time_it

from itertools import combinations

from pprint import pprint


EXPANSION = 1  # x 2


def get_galaxy_coords(data_lines: list[str]) -> list[tuple[int, int]]:
    """finds the coordinates of all galaxies in the universe"""
    return [(r, c) for r, row in enumerate(data_lines) for c, cell in enumerate(row) if cell == GALAXY]


def expand_galaxies(galaxies: list[tuple[int, int]], expansion: int = EXPANSION) -> list[tuple[int, int]]:
    expanded_galaxies = []

    empty_rows = set(range(max(coords[0] for coords in galaxies) + 1)) - set(coords[0] for coords in galaxies)
    empty_cols = set(range(max(coords[1] for coords in galaxies) + 1)) - set(coords[1] for coords in galaxies)

    for r, c in galaxies:
        row_expand = len([row for row in empty_rows if row < r])  # how many empty rows are before current row
        col_expand = len([col for col in empty_cols if col < c])  # how many empty cols are before current col
        expanded_galaxies.append((r + expansion * row_expand, c + expansion * col_expand))

    return expanded_galaxies


def shortest_path(first: tuple[int, int], second: tuple[int, int]) -> int:
    """finds the shortest path between 2 galaxies in the universe
    returns the number of steps between first and second"""

    # special case: horizontal line
    if (second[1] - first[1]) == 0:
        return abs(second[0] - first[0])

    # special case: vertical line
    if (second[0] - first[0]) == 0:
        return abs(second[1] - first[1])

    # calculate slope m and offset q for line with formula y = mx + q
    m = (second[1] - first[1]) / (second[0] - first[0])
    q = first[1] - m * first[0]

    new_coords = []

    if abs(m) < 1:  # more horizontal - loop over x and calculate y
        coords = [(x, round(m * x + q)) for x in range(min(first[0], second[0]), max(first[0], second[0]) + 1)]
        # fill in a step where both coordinates jump at the same time
        for pair in zip(coords, coords[1:]):
            new_coords.append(pair[0])  # add the first coord of the pair
            if abs(pair[0][0] - pair[1][0]) > 0 and abs(pair[0][1] - pair[1][1]):
                new_coords.append((pair[1][0], pair[0][1]))  # add intermediate coord
        new_coords.append(coords[-1])  # add the final coord
    else:  # more vertical - loop over y and calculate x
        coords = [(round((y - q) / m), y) for y in range(min(first[1], second[1]), max(first[1], second[1]) + 1)]
        # fill in a step where both coordinates jump at the same time
        for pair in zip(coords, coords[1:]):
            new_coords.append(pair[0])  # add the first coord of the pair
            if abs(pair[0][0] - pair[1][0]) > 0 and abs(pair[0][1] - pair[1][1]):
                new_coords.append((pair[0][0], pair[1][1]))  # add intermediate coord
        new_coords.append(coords[-1])  # add the final coord

    return len(new_coords) -1


def draw_universe(galaxies: list[tuple[int, int]]) -> None:
    """draws the universe"""
    for r in range(max(coords[0] for coords in galaxies) + 1):
        for c in range(max(coords[1] for coords in galaxies) + 1):
            if (r, c) in galaxies:
                print(GALAXY, end='')
            else:
                print(EMPTY_SPACE, end='')
        print()
    print('-' * 100)


@time_it
def main(data_lines: list[str]) -> None:
    galaxies = get_galaxy_coords(data_lines)
    # print(galaxies)
    # draw_universe(galaxies)

    expanded_galaxies = expand_galaxies(galaxies)
    # print(expanded_galaxies)
    # draw_universe(expanded_galaxies)

    path_lengths = []
    for pair in combinations(expanded_galaxies, 2):
        path_length = shortest_path(*pair)
        # print(pair, path_length)
        path_lengths.append(path_length)

    print(f'End result: {sum(path_lengths)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 374
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 9947476
    #   Finished 'main' in 3.2 seconds

    # test_universe = [(9, 9)]
    # draw_universe(test_universe)

    # # testing shortest_path
    # for test in (
    #         ((1, 1), (1, 8)),  # vertical
    #         ((1, 1), (8, 1)),  # horizontal
    #         ((1, 1), (8, 8)),  # m=1
    #         ((1, 8), (8, 1)),  # m=-1
    #         ((2, 1), (8, 4)),  # m=1/2
    #         ((2, 4), (8, 1)),  # m=-1/2
    #         ((1, 2), (4, 8)),  # m=2
    #         ((10, 10), (80, 80)),  # m=1
    #         ((20, 10), (80, 40)),  # m=1/2
    #         ((10, 20), (40, 80)),  # m=2
    #         ((100, 100), (800, 800)),  # m=1
    #         ((200, 100), (800, 400)),  # m=1/2
    #         ((100, 200), (400, 800)),  # m=2
    #         ((1000000, 2000000), (4000000, 8000000)),  # m=2
    # ):
    #     print(test, shortest_path(*test))

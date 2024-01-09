# aoc_2023_11_B.py - Day 11: Cosmic Expansion - part 2
# sum the shortest paths between galaxies in a massively expanded universe
# even with the refactoring in aoc_2023_11_A_2, the shortest_path function is still creating arrays for
# every line that is 'drawn' between galaxies. with galaxy coordinates in the millions this is no longer feasible,
# so we need a way to calculate the number of steps instead of calculating every step's coordinates
# https://adventofcode.com/2023/day/11


from aoc_2023_11_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    EMPTY_SPACE,
    GALAXY,
    PATH,
)

from aoc_2023_11_A_2 import (
    expand_galaxies,
    get_galaxy_coords,
)

from itertools import combinations


# EXPANSION = 1  # x 2
# EXPANSION = 9  # x 10
# EXPANSION = 99  # x 100
EXPANSION = 999_999  # x 1_000_000


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

    if abs(m) < 1:  # more horizontal - base number = x2 - x1, multiply that with 1 + m to get result
        return round(abs(second[0] - first[0]) * (1 + abs(m)))
    else:  # more vertical - base number = y2 - y1, multiply that with 1 + 1/m to get result
        return round(abs(second[1] - first[1]) * (1 + 1 / abs(m)))


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    galaxies = get_galaxy_coords(data_lines)
    # print(galaxies)

    expanded_galaxies = expand_galaxies(galaxies, EXPANSION)
    # print(expanded_galaxies)

    # # testing shortest_path
    # for test in (
    #         # ((1, 1), (1, 8)),  # (7) vertical
    #         # ((1, 1), (8, 1)),  # (7) horizontal
    #         ((1, 1), (8, 8)),  # (14) m=1
    #         # ((1, 8), (8, 1)),  # (14) m=-1
    #         ((2, 1), (8, 4)),  # (9) m=1/2
    #         # ((2, 4), (8, 1)),  # (9) m=-1/2
    #         ((1, 2), (4, 8)),  # (9) m=2
    #         ((10, 10), (80, 80)),  # (140) m=1
    #         ((20, 10), (80, 40)),  # (90) m=1/2
    #         ((10, 20), (40, 80)),  # (90) m=2
    #         ((100, 100), (800, 800)),  # m=1
    #         ((200, 100), (800, 400)),  # m=1/2
    #         ((100, 200), (400, 800)),  # m=2
    #         ((1000000, 2000000), (4000000, 8000000)),  # m=2
    # ):
    #     print(test, shortest_path(*test))

    path_lengths = []
    for pair in combinations(expanded_galaxies, 2):
        path_length = shortest_path(*pair)
        # print(pair, path_length)
        path_lengths.append(path_length)

    print(f'End result: {sum(path_lengths)}')

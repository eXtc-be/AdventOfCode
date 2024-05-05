# aoc_2023_17_A_1.py - Day 17: Clumsy Crucible - part 1
# Directing the crucible from the lava pool to the machine parts factory,
# but not moving more than three consecutive blocks in the same direction,
# what is the least heat loss it can incur?
# https://adventofcode.com/2023/day/17


from tools import time_it

from sys import maxsize
from itertools import groupby

from pprint import pprint


DATA_PATH = './input_2023_17'

# DIRECTIONS: dict[str, tuple[int, int]] = {
#     'U': (-1, 0),
#     'D': (1, 0),
#     'L': (0, -1),
#     'R': (0, 1),
# }

# prefer to go right and down first
DIRECTIONS: dict[str, tuple[int, int]] = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}

MAX_STREAK = 3

# formatting codes
HEADER = '\033[95m'  # (magenta)
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'  # (orange)
FAIL = '\033[91m'  # (red)

BOLD = '\033[1m'
UNDERLINE = '\033[4m'

ENDC = '\033[0m'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_grid(data_lines: list[str]) -> list[list[int]]:
    return [[int(char) for char in line] for line in data_lines]


def _bold(string: str) -> str:
    """returns the string prepended with BOLD or FAIL and appended with ENDC"""
    return BOLD + string + ENDC


def _red(string: str) -> str:
    """returns the string prepended with BOLD or FAIL and appended with ENDC"""
    return FAIL + string + ENDC


def _blue(string: str) -> str:
    """returns the string prepended with BOLD or FAIL and appended with ENDC"""
    return OKBLUE + string + ENDC


def _orange(string: str) -> str:
    """returns the string prepended with BOLD or FAIL and appended with ENDC"""
    return WARNING + string + ENDC


def draw_grid(
        grid: list[list[int]],
        parents: dict[tuple[int, int], tuple[int, int]] = [],
        path: list[tuple[int, int]] = [],
        current: tuple[int, int] = None
) -> None:
    """draws the grid and highlights the parents (and the path) and the current node, if given"""
    if parents and not path:
        path = _get_path(parents, current)
    for rr, row in enumerate(grid):
        print(''.join((
            _red(str(value)) if (rr, cc) == current else _orange(str(value)) if (rr, cc) in path else _blue(str(value)) if (rr, cc) in parents else str(value)
            for cc, value in enumerate(row))
        ))
    print('-' * 100)


def _good_streak(numbers: list[tuple[int, int]]) -> bool:
    """calculates the number of consecutive identical numbers in a list of coordinates"""
    r_streak = max(len(list(grp)) for _, grp in groupby(number[0] for number in numbers[-(MAX_STREAK + 2):]))
    c_streak = max(len(list(grp)) for _, grp in groupby(number[1] for number in numbers[-(MAX_STREAK + 2):]))
    return max(r_streak, c_streak) <= MAX_STREAK + 1  # +1 because the first node after a turn does not count for the streak


def _get_neighbors(
        grid: list[list[int]],
        path: list[tuple[int, int]],
        node: tuple[int, int]
) -> list[tuple[tuple[int, int], int]]:
    """returns an array of neighbors for a given node,
    considering the 'no more than MAX_STREAK steps in the same direction' rule"""
    neighbours = []
    for rr, cc in DIRECTIONS.values():
        if 0 <= node[0] + rr < len(grid) and 0 <= node[1] + cc < len(grid[node[0] + rr]):
            if _good_streak(path+[(node[0] + rr, node[1] + cc)]):
                neighbours.append(((node[0] + rr, node[1] + cc), grid[node[0] + rr][node[1] + cc]))

    return neighbours
    # return [
    #     ((node[0] + rr, node[1] + cc), grid[node[0] + rr][node[1] + cc])
    #     for rr, cc in DIRECTIONS.values()
    #     if 0 <= node[0] + rr < len(grid) and 0 <= node[1] + cc < len(grid[rr])
    # ]


def _get_path(parents: dict[tuple[int, int], tuple[int, int]], node: tuple[int, int]) -> list[tuple[int, int]]:
    """from a linked list of parents, constructs the list of nodes from the start to the given node"""
    path = []

    while parents[node] != node:
        path.append(node)
        node = parents[node]

    path.append(parents[node])

    path.reverse()

    return path


def _h(grid: list[list[int]], current: tuple[int, int], target: tuple[int, int]) -> int:
    """
    returns the Manhattan distance between current and target
    https://en.wikipedia.org/wiki/Taxicab_geometry
    """
    return abs(target[0] - current[0]) + abs(target[1] - current[1])


def find_path(grid: list[list[int]], start: tuple[int, int], stop: tuple[int, int]) -> list[tuple[int, int]] | None:
    """
    finds the path with the least heat loss from start to end
    without going more than 3 consecutive times in the same direction
    using the A* algorithm
    """
    to_visit = [start]
    visited = []
    g = {start: 0}
    parents = {start: start}

    while to_visit:
        n = None

        for v in to_visit:
            if (
                n is None or
                g[v] + _h(grid, v, stop) < g[n] + _h(grid, n, stop)
            ):
                n = v

        # draw_grid(grid, parents=parents, current=n)

        # n is guaranteed to not be None:
        #   - while to_visit assures there is at least one node to do: for v in to_visit
        #   - if n is None: n = v assures the first node in to_visit is always considered
        # if n is None:
        #     return None

        if n == stop:
            return _get_path(parents, n)

        for (m, weight) in _get_neighbors(grid, _get_path(parents, n), n):
            if m not in to_visit and m not in visited:
                to_visit.append(m)
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n

                    if m in visited:
                        visited.remove(m)
                        to_visit.append(m)

        # remove n from the to_visit, and add it to visited
        to_visit.remove(n)
        visited.append(n)

    return None


# test_data = '''
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# '''.strip().splitlines()


# test_data = '''
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# 111111111111
# '''.strip().splitlines()


# test_data = '''
# 24134
# 32154
# 32552
# '''.strip().splitlines()


test_data = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)
    # draw_grid(grid)

    path = find_path(grid, (0, 0), (len(grid)-1, len(grid[len(grid)-1])-1))
    if path is None:
        print("No path found!")
    else:
        print('Found a path:', path)
        # draw_grid(grid, path)
        weights = [grid[n[0]][n[1]] for n in path]
        # print('Weights:', weights)
        print(f'End result: {sum(weights[1:])}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: 113 (should be 102)
    #   Finished 'main' in 5 milliseconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

    # # test _get_neighbors
    # grid = create_grid(data_lines)
    # for rr, row in enumerate(grid):
    #     for cc, cell in enumerate(row):
    #         print((rr, cc), _get_neighbors(grid,(rr, cc)))

    # # test _calc_streak
    # for test in [
    #     [(0, 1), (2, 3), (4, 5), (6, 7)],
    #     [(0, 1), (1, 2), (2, 2), (3, 4), (5, 6)],
    #     [(0, 1), (1, 1), (1, 2), (1, 3), (5, 6)]
    # ]:
    #     print(test, _calc_streak(test))

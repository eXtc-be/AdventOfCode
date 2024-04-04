# aoc_2018_18_A_1.py - Day 18: Settlers of The North Pole - part 1
# What will the total resource value of the lumber collection area be after 10 minutes?
# https://adventofcode.com/2018/day/18


from tools import time_it

import os

from pprint import pprint


DATA_PATH = './input_2018_18'

DIRECTIONS = [
    (-1, -1),   # up left
    (-1, 0),    # up
    (-1, 1),    # up right
    (0, -1),    # left
    (0, 1),     # right
    (1, -1),    # down left
    (1, 0),     # down
    (1, 1),     # down right
]

OPEN = '.'
TREES = '|'
YARD = '#'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_grid(data_lines: list[str]) -> list[list[str]]:
    return [[char for char in line] for line in data_lines]


def print_grid(grid: list[list[str]]) -> None:
    for row in grid:
        print(''.join(row))


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear') if not os.environ.get('CHARM') else print('-' * 100)


def _get_neighbors(grid: list[list[str]], position) -> str:
    max_r, max_c = len(grid), len(grid[0])

    return ''.join(
        grid[position[0]+direction[0]][position[1]+direction[1]]
        for direction in DIRECTIONS
        if 0 <= position[0] + direction[0] < max_r and 0 <= position[1] + direction[1] < max_c
    )


def do_step(grid: list[list[str]]) -> list[list[str]]:
    new_grid = []

    for r, row in enumerate(grid):
        new_row = []
        for c, cell in enumerate(row):
            neighbors = _get_neighbors(grid, (r, c))
            if cell == OPEN:
                if neighbors.count(TREES) >= 3:
                    new_row.append(TREES)
                else:
                    new_row.append(OPEN)
            elif cell == TREES:
                if neighbors.count(YARD) >= 3:
                    new_row.append(YARD)
                else:
                    new_row.append(TREES)
            elif cell == YARD:
                if neighbors.count(YARD) >= 1 and neighbors.count(TREES) >= 1:
                    new_row.append(YARD)
                else:
                    new_row.append(OPEN)
            else:
                print(f'Unknown cell: "{cell}"')
        new_grid.append(new_row)

    return new_grid


def score_grid(grid: list[list[str]]) -> int:
    return sum(line.count(TREES) for line in grid) * sum(line.count(YARD) for line in grid)


test_data = '''
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], verbose: bool = False) -> None:
    grid = get_grid(data_lines)
    # pprint(grid)

    if verbose:
        print(f'Step: 0')
        print_grid(grid)

    for step in range(100):
        if verbose:
            input('Press Enter to continue...')
            clear()
            print(f'Step: {step + 1} - Score: {score_grid(grid)}')
            print_grid(grid)
        grid = do_step(grid)

    print(f'\nEnd result: {score_grid(grid)}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data, verbose=True)

    # using test_data:
    #   End result: 1147
    #   Finished 'main' in 3 milliseconds
    # using input data:
    #   End result: 598416
    #   Finished 'main' in 75 milliseconds

    # # test _get_neighbors
    # grid = get_grid(test_data)
    # for r, row in enumerate(grid):
    #     for c, char in enumerate(row):
    #         print(char, (r, c), _get_neighbors(grid, (r, c)))


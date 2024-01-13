# aoc_2015_18_A_1.py - Day 18: Like a GIF For Your Yard - part 1
# In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?
# https://adventofcode.com/2015/day/18


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_18'

STEPS = 100

OFF = '.'
ON = '#'

DIRECTIONS = {
    'UP': (-1, 0),
    'UL': (-1, -1),
    'LE': (0, -1),
    'DL': (1, -1),
    'DN': (1, 0),
    'DR': (1, 1),
    'RI': (0, 1),
    'UR': (-1, 1),
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_grid(data_lines: list[str]) -> list[list[str]]:
    return [[char for char in line] for line in data_lines]


def _count_neighbours(r:int , c:int , grid: list[list[str]]) -> int:
    count = 0

    for direction in DIRECTIONS.values():
        if 0 <= r + direction[0] <= len(grid) - 1 and 0 <= c + direction[1] <= len(grid[r]) - 1:
            if grid[r + direction[0]][c + direction[1]] == ON:
                count += 1

    return count


def do_step(grid: list[list[str]]) -> list[list[str]]:
    result = []
    for r, row in enumerate(grid):
        result_row = []
        for c, cell in enumerate(row):
            neighbours = _count_neighbours(r, c, grid)
            if cell == ON:
                if neighbours in (2, 3):
                    result_row.append(ON)
                else:
                    result_row.append(OFF)
            else:
                if neighbours == 3:
                    result_row.append(ON)
                else:
                    result_row.append(OFF)
        result.append(result_row)

    return result


test_data = '''
.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    grid = get_grid(data_lines)
    # print(grid)
    # print('\n'.join(''.join(char for char in row) for row in grid))
    # print('=' * 100)

    new_grid = grid  # initial value
    for _ in range(STEPS):
        new_grid = do_step(new_grid)
        # print('\n'.join(''.join(char for char in row) for row in new_grid))
        # print('-' * 100)

    print(f'End result: {sum(row.count(ON) for row in new_grid)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 768
    #   Finished 'main' in 2.2 seconds

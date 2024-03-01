# aoc_2017_21_A_1.py - Day 21: Fractal Art - part 1
# How many pixels stay on after 5 iterations?
# https://adventofcode.com/2017/day/21


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_21'

START = """
.#.
..#
###
""".strip().splitlines()

ROUNDS = 5
ROUNDS_TEST = 2


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _transform(src: list[str]) -> list[str]:
    # no change
    yield src

    # horizontal flip
    yield [l[::-1] for l in src]

    # vertical flip
    yield src[::-1]

    # horizontal + vertical flip
    yield [l[::-1] for l in src[::-1]]

    # create a list of lists
    arr = [[c for c in row] for row in src]
    # swap rows and columns and re-create list of strings
    rot = [''.join(r) for r in zip(*arr)]

    # rows to columns (rotate ??)
    yield rot

    # horizontal flip
    yield [l[::-1] for l in rot]

    # vertical flip
    yield rot[::-1]

    # horizontal + vertical flip
    yield [l[::-1] for l in rot[::-1]]


def _find_rule(rules: list[str], src: list[str]) -> list[str]:
    for rule in rules:
        if len(rule.split(' => ')[0].split('/')) == len(src):
            for var in _transform(rule.split(' => ')[0].split('/')):
                if src == var:
                    return rule.split(' => ')[1].split('/')


def _divide(grid: list[str], size: int) -> list[list[str]]:
    for r in range(0, len(grid), size):
        for c in range(0, len(grid[r]), size):
            yield [row[c:c+size] for row in grid[r:r+size]]


def enhance(grid: list[str], rules: list[str]) -> list[str]:
    if len(grid) == 2 or len(grid[0]) == 3:
        return _find_rule(rules, grid)

    if len(grid) % 2 == 0:
        factor = len(grid) // 2
        result = [['O' for _ in range(factor * 3)] for _ in range(factor * 3)]
        for i, sub_grid in enumerate(_divide(grid, 2)):
            dst = _find_rule(rules, sub_grid)
            for r, row in enumerate(dst):
                result[(i // factor) * 3 + r][(i % factor) * 3:(i % factor) * 3 + 3] = row
        return [''.join(row) for row in result]
    elif len(grid) % 3 == 0:
        factor = len(grid) // 3
        result = [['O' for _ in range(factor * 4)] for _ in range(factor * 4)]
        for i, sub_grid in enumerate(_divide(grid, 3)):
            dst = _find_rule(rules, sub_grid)
            for r, row in enumerate(dst):
                result[(i // factor) * 4 + r][(i % factor) * 4:(i % factor) * 4 + 4] = row
        return [''.join(row) for row in result]


test_data = '''
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    src = START
    dst = None

    for round in range(rounds):
        # print('\n'.join(src))
        # print('-' * 100)

        dst = enhance(src, data_lines)
        # print('\n'.join(dst))
        # print('=' * 100)

        src = dst

    print(f'End result: {sum(row.count("#") for row in dst)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, ROUNDS_TEST)
    # using test_data:
    #   End result: 12
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 190
    #   Finished 'main' in 5 milliseconds

    # # test _transform
    # for var in _transform('#./..'.split('/')):
    #     print('\n'.join(var))
    #     print('-' * 100)
    #
    # for var in _transform(START):
    #     print('\n'.join(var))
    #     print('-' * 100)

    # # test _divide
    # grid = ['0123', '4567', '89ab', 'cdef']
    # print('\n'.join(grid))
    # print('-' * 100)
    # for sub_grid in _divide(grid, 2):
    #     print('\n'.join(sub_grid))
    #     print('-' * 100)
    #
    # grid = ['012345', '6789ab', 'cdef01', '234567', '89abcd', 'ef0123']
    # print('\n'.join(grid))
    # print('-' * 100)
    # for sub_grid in _divide(grid, 2):
    #     print('\n'.join(sub_grid))
    #     print('-' * 100)
    #
    # grid = ['012345', '6789ab', 'cdef01', '234567', '89abcd', 'ef0123']
    # print('\n'.join(grid))
    # print('-' * 100)
    # for sub_grid in _divide(grid, 3):
    #     print('\n'.join(sub_grid))
    #     print('-' * 100)

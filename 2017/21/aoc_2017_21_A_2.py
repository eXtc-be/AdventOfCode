# aoc_2017_21_A_2.py - Day 21: Fractal Art - part 1
# How many pixels stay on after 5 iterations?
# https://adventofcode.com/2017/day/21
# optimization: instead of generating all transformations for a given sub-grid each time,
#               we pre-calculate all variations for all rules once and use those


from aoc_2017_21_A_1 import (
    DATA_PATH,
    START,
    ROUNDS,
    ROUNDS_TEST,
    load_data,
    test_data,
    _transform,_divide
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def get_rules(data_lines: list[str]) -> dict[str, str]:
    rules = {}

    for line in data_lines:
        src, dst = line.split(' => ')
        src = src.split('/')
        for var in _transform(src):
            rules['/'.join(var)] = dst

    return rules


def enhance(grid: list[str], rules: dict[str, str]) -> list[str]:
    if len(grid) == 2 or len(grid[0]) == 3:
        return rules['/'.join(grid)].split('/')

    if len(grid) % 2 == 0:
        factor = len(grid) // 2
        result = [['O' for _ in range(factor * 3)] for _ in range(factor * 3)]
        for i, sub_grid in enumerate(_divide(grid, 2)):
            dst = rules['/'.join(sub_grid)].split('/')
            for r, row in enumerate(dst):
                result[(i // factor) * 3 + r][(i % factor) * 3:(i % factor) * 3 + 3] = row
        return [''.join(row) for row in result]
    elif len(grid) % 3 == 0:
        factor = len(grid) // 3
        result = [['O' for _ in range(factor * 4)] for _ in range(factor * 4)]
        for i, sub_grid in enumerate(_divide(grid, 3)):
            dst = rules['/'.join(sub_grid)].split('/')
            for r, row in enumerate(dst):
                result[(i // factor) * 4 + r][(i % factor) * 4:(i % factor) * 4 + 4] = row
        return [''.join(row) for row in result]


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    rules = get_rules(data_lines)
    # pprint(rules)

    src = START
    dst = None

    for round in range(rounds):
        # print('\n'.join(src))
        # print('-' * 100)

        dst = enhance(src, rules)
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
    #   Finished 'main' in 2 milliseconds

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

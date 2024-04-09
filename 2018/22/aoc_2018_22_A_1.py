# aoc_2018_22_A_1.py - Day 22: Mode Maze - part 1
# What is the total risk level for the smallest rectangle that includes 0,0 and the target's coordinates?
# https://adventofcode.com/2018/day/22


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_22'

Y_0 = 16807
X_0 = 48271
MODULO = 20183

TYPES = {
    0: '.',
    1: '=',
    2: '|',
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_inputs(data_lines: list[str]) -> tuple[int, tuple[int, int]]:
    return (
        int(data_lines[0].split()[1]),
        (int(data_lines[1].split()[1].split(',')[0]), int(data_lines[1].split()[1].split(',')[1])),
    )


def _get_levels(depth: int, target: tuple[int, int]) -> list[list[int]]:
    levels = [[0 for c in range(target[0]+1)] for r in range(target[1]+1)]
    val = 0

    for y in range(target[1]+1):
        for x in range(target[0]+1):
            if (x, y) == (0, 0) or (x, y) == target:
                val = 0
            elif y == 0:
                val = x * Y_0
            elif x == 0:
                val = y * X_0
            else:
                val = levels[y][x-1] * levels[y-1][x]

            levels[y][x] = (val + depth) % MODULO

    return levels


def _get_types(depth: int, target: tuple[int, int]) -> list[list[int]]:
    return [[level % 3 for level in row] for row in _get_levels(depth, target)]


def calc_risk(depth: int, target: tuple[int, int]) -> int:
    return sum(sum(row) for row in _get_types(depth, target))


def draw_grid(types: list[list[int]]) -> None:
    print('\n'.join(
        ''.join(TYPES[t] for t in row)
        for row in types
    ))


test_data = '''
depth: 510
target: 10,10
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    depth, target = get_inputs(data_lines)
    # print(depth, target)

    # types = _get_types(depth, target)
    # pprint(types)

    # draw_grid(types)

    print(f'End result: {calc_risk(depth, target)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 114
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 9940
    #   Finished 'main' in 5 milliseconds

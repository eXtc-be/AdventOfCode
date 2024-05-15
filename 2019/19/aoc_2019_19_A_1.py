# aoc_2019_19_A_1.py - Day 19: Tractor Beam - part 1
# How many points are affected by the tractor beam in the 50x50 area closest to the emitter?
# https://adventofcode.com/2019/day/19
# I created 2 versions of main:
#   one where I reuse the same computer, but reinitialize its memory and instruction pointer;
#   and one where I create a new computer every time the double loop executes
# the second version runs twice as fast as the first


from tools import time_it
from intcode import Computer

# other imports

from pprint import pprint


DATA_PATH = './input_2019_19'

GRID = '50x50'

BEAM = '.#'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


# @time_it
# def main(intcode: str, grid_size: str = GRID, verbose: bool = False, confirm: bool = False) -> None:
#     total = 0
#
#     computer = Computer([], [], False)
#
#     rows, cols = map(int, grid_size.split('x'))
#
#     for r in range(rows):
#         for c in range(cols):
#             computer.memory = list(map(int, intcode.split(',')))
#             computer.ip = 0
#             computer.run([c, r])
#             if verbose:
#                 print(BEAM[computer.outputs[0]], end='')
#             total += computer.outputs[0]
#             computer.outputs = []
#         if verbose:
#             print()
#
#     print(f'End result: {total}')


@time_it
def main(intcode: str, grid_size: str = GRID, verbose: bool = False, confirm: bool = False) -> None:
    total = 0

    rows, cols = map(int, grid_size.split('x'))

    for r in range(rows):
        for c in range(cols):
            computer = Computer(list(map(int, intcode.split(','))), [], False)
            computer.run([c, r])
            if verbose:
                print(BEAM[computer.outputs[0]], end='')
            total += computer.outputs[0]
        if verbose:
            print()

    print(f'End result: {total}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0], GRID, True)
    # main(load_data(DATA_PATH)[0])
    # main(load_data(DATA_PATH)[0], "100x100", True)
    # main(load_data(DATA_PATH)[0], '10x10', False)

    # using 10x10 grid:
    #   End result: 7
    #   Finished 'main' in 1 second re-using/resetting computer
    #   Finished 'main' in 404 milliseconds creating a new computer each time
    # using input data:
    #   End result: 203
    #   Finished 'main' in 5.2 seconds

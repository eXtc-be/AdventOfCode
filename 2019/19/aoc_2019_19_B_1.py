# aoc_2019_19_B_1.py - Day 19: Tractor Beam - part 2
# Find the 100x100 square closest to the emitter that fits entirely within the tractor beam;
# within that square, find the point closest to the emitter.
# What value do you get if you take that point's X coordinate, multiply it by 10000, then add the point's Y coordinate?
# https://adventofcode.com/2019/day/19

# at first, I was going to calculate the slopes of the 2 lines that make up the beam and use those to calculate
# all horizontal and vertical distances needed to determine at what row the beam is wide enough to contain the ship,
# but, although this worked perfectly on paper, the rounding errors made this almost impossible to program (I can
# still use those calculations to find the ballpark number for my final solution), so this version starts from
# row 90 (I calculated it would be around 100 for a ship of width 10) and works its way up (down?) until the beam
# is wide enough to fit a ship that size. of course this will not work fast enough for the actual puzzle,
# but will help to give a feel for what to expect in the next versions (I already found that several vertical distances
# yield the same result for check_beam_width).
# this version uses the computer twice (per loop) to determine the width of the beam at a certain vertical distance and
# at that distance + the height of the ship. it then calculates the difference between the number of units needed
# and the number of units available to help determine if we should go up or down (this is not used in this version,
# as it only goes up atm, but will be used in a next version that uses binary search)
#
# I managed to calculate the ballpark number and by manually tweaking get close enough to find the correct value for the
# real puzzle input. when I tried it on the site it said the value was too high.
# I then printed out that section of the beam to confirm by hand that a 100x100 square could indeed fit. I discovered
# that my x value was off by one, so when I tried submitting the new value, it passed.


from aoc_2019_19_A_1 import (
    DATA_PATH,
    BEAM,
    load_data,
)

from tools import time_it
from intcode import Computer

# other imports

from pprint import pprint


SHIP = 100


def get_beam_width(y: int, verbose: bool = False) -> tuple[int, int]:
    """returns the beam's edges' horizontal coordinates at vertical distance y"""
    x1 = None
    x2 = None

    x = 0
    while True:
        computer = Computer(list(map(int, load_data(DATA_PATH)[0].split(','))), [], False)
        computer.run([x, y])
        if x1 is None and computer.outputs[0] == 1:
            x1 = x  # found the first x where the beam is active
        elif x1 is not None and computer.outputs[0] == 0:
            x2 = x
            break
        if verbose:
            print(BEAM[computer.outputs[0]], end='')
        x += 1
    if verbose:
        print()
    return x1, x2


def check_beam_width(y: int, dim: int, verbose: bool = False) -> int:
    """checks whether the beam is wide enough to contain a ship of dim x dim units
    returns the difference between the actual beam width and the minimum width"""

    # for i in range(dim):
    #     _, _ = get_beam_width(y + i, verbose)

    _, x12 = get_beam_width(y, verbose)
    x21, _ = get_beam_width(y + dim - 1, verbose)
    return x12 - x21 - dim


@time_it
def main(start: int, dim: int = SHIP, verbose: bool = False) -> None:
    y = start

    while True:
        if verbose:
            print(y)
        result = check_beam_width(y, dim, verbose)
        if verbose:
            print(result)
            print()
        if result == 0:
            break
        y += 1

    # I could have check_beam_width return the value of x12, but at this point I don't mind
    # calling get_beam_width one last time instead of making things complicated

    # _, x12 = get_beam_width(y, verbose)
    # print(f'End result: {y + 10000 * (x12 - dim + 1)}')

    x21, _ = get_beam_width(y + dim, verbose)
    # print(f'End result: {y + 10000 * x21}')  # off by one error
    print(f'End result: {y + 10000 * (x21 - 1)}')


if __name__ == "__main__":
    # main()
    # main(90, 10, True)  # calculations suggest vertical distance is 105
    main(1050, 100, True)  # calculations suggest vertical distance is 1094, tests suggest it is between 1050 and 1094

    # using ship width 10:
    #   End result: 830099 (x=83, y=99)
    #   Finished 'main' in 8.0 seconds
    # using ship width 100:
    #   End result: 8781057 (x=878, y=1057) - too high
    #   End result: 8771057 (x=877, y=1057) - correct
    #   Finished 'main' in 1 minute and 11 seconds

    # x1, x2 = get_beam_width(100, True)
    # print(x1, x2, x2 - x1)

    # print(check_beam_width(103, 10, True))

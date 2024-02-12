# aoc_2016_11_B_1.py - Day 11: Radioisotope Thermoelectric Generators - part 2
# In your situation, what is the minimum number of steps required to bring all the objects to the fourth floor?
# https://adventofcode.com/2016/day/11


from aoc_2016_11_A_1 import (
    TEST_LAYOUT,
    main,
)

from curses import wrapper

from pprint import pprint


REAL_LAYOUT = {
    'PoG': 1,
    'PoM': 2,
    'TmG': 1,
    'TmM': 1,
    'PmG': 1,
    'PmM': 2,
    'RuG': 1,
    'RuM': 1,
    'CoG': 1,
    'CoM': 1,
    'ElG': 1,
    'ElM': 1,
    'DiG': 1,
    'DiM': 1,
}


# other functions


if __name__ == "__main__":
    layout = REAL_LAYOUT
    # layout = TEST_LAYOUT
    # print(layout)

    wrapper(main, layout)
    # using input data:
    #   End result: xxx

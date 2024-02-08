# aoc_2015_25_A_1.py - Day 25: Let It Snow - part 1
# Santa looks nervous.  Your puzzle input contains the message on the machine's console.
# What code do you give the machine?
# https://adventofcode.com/2015/day/25


import sys
sys.path.insert(0, '../..')

from tools import time_it

# other imports

from pprint import pprint


SEED = 20_151_125
MULTI = 252_533
MODULO = 33_554_393


def calculate_next(num: int) -> int:
    return (num * MULTI) % MODULO


@time_it
def main(row, col) -> None:
    diagonal = (row - 1) + (col - 1)
    index = sum(n+1 for n in range(diagonal)) + (col - 1)
    l1 = len(f'{index:,}')
    l2 = len(f'{MODULO:,}')
    # print(index)

    num = SEED
    for i in range(index):
        print(f'{i:{l1},} / {index:{l1},} -> {num:{l2},}')
        num = calculate_next(num)

    print(f'End result: {num}')


if __name__ == "__main__":
    row, col = 2947, 3029
    # row, col = 4, 4

    main(row, col)
    # using input data:
    #   End result: 19980801
    #   Finished 'main' in 22 minutes and 14 seconds

    # for row in range(1, 7):
    #     for col in range(1, 7):
    #         print(row, col)
    #         main(row, col)
    #         print('-' * 100)

# aoc_2018_02_B_1.py - Day 2: Inventory Management System - part 2
# What is the checksum for your list of box IDs?
# https://adventofcode.com/2018/day/2


from aoc_2018_02_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
)

from tools import time_it

from itertools import combinations

from pprint import pprint


# other constants


def compare_strings(first: str, second: str) -> str:
    return ''.join(first[i] for i in range(len(first)) if first[i] == second[i])


test_data = '''
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    comp = ''
    for combo in combinations(data_lines, 2):
        comp = compare_strings(combo[0], combo[1])
        # print(combo, comp)
        if len(comp) == len(combo[0])-1:
            break

    print(f'End result: {comp}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: fgij
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: jiwamotgsfrudclzbyzkhlrvp
    #   Finished 'main' in 30 milliseconds

# aoc_2015_08_B_1.py - Day 8: Matchsticks - part 2
# What is the total number of characters to represent
# the newly encoded strings minus the number of characters of code
# in each original string literal?
# https://adventofcode.com/2015/day/8


from aoc_2015_08_A_1 import (
    DATA_PATH,
    load_data,
    REP_SLASH,
    REP_QUOTE
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def get_increase(string: str) -> int:
    increase = 0

    increase += string.count(REP_SLASH)
    increase += string.count(REP_QUOTE)

    return increase


@time_it
def main(data_lines: list[str]) -> None:
    differences = []
    for string in data_lines:
        differences.append(get_increase(string))
    print(differences)

    print(f'End result: {sum(differences) + 2 * len(differences)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = load_data('test_data')
    print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

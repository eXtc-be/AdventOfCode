# aoc_2015_11_B_1.py - Day 11: Corporate Policy - part 2
# Given Santa's current password, what should his next password be?
# https://adventofcode.com/2015/day/11


from aoc_2015_11_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    generate_new_pw,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    new_pw = ''
    for line in data_lines:
        new_pw = generate_new_pw(line)
        print(f'{line} -> {new_pw}')
        new_pw = generate_new_pw(new_pw)
        print(f'{line} -> {new_pw}')

    print(f'End result: {new_pw}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

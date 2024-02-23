# aoc_2017_09_B_1.py - Day 9: Stream Processing - part 2
# How many non-canceled characters are within the garbage in your puzzle input?
# https://adventofcode.com/2017/day/9


from aoc_2017_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    test_garbage,
    _find_garbage,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def _count_garbage(string: str) -> int:
    total = 0
    cancel_next = False

    for char in string[1:-1]:
        if cancel_next:
            cancel_next = False
            # don't increment
        else:
            if char == '!':
                cancel_next = True
                # don't increment
            else:
                total += 1

    return total


def count_all_garbage(string: str) -> int:
    total = 0

    while True:
        start, stop = _find_garbage(string)
        if start < 0 or stop < 0:  # no more garbage found
            break
        total += _count_garbage(string[start:stop])
        string = string[:start] + string[stop:]

    return total



@time_it
def main(data_lines: list[str]) -> None:
    # # test _count_garbage
    # for line in test_garbage:
    #     print(line, _count_garbage(line))

    # # test count_all_garbage
    # for line in test_garbage:
    #     print(line, count_all_garbage(line))

    # test count_all_garbage
    for line in data_lines:
        print(line, count_all_garbage(line))

    # print(f'End result: {count_all_garbage(data_lines[0])}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 0, 0, 0, 0, 0, 10, 4, 4, 8, 0, 13, 17
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 9978
    #   Finished 'main' in 226 milliseconds

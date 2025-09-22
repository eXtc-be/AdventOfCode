# aoc_2024_01_B_1.py - Day 1: Historian Hysteria - part 2
# What is your lists similarity score?
# https://adventofcode.com/2024/day/1


from aoc_2024_01_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_lists,
)

from tools import time_it

# other imports

from pprint import pprint
from collections import Counter


# other constants


# other functions

def calc_similarity(l1: list[int], d2: dict[int, int]) -> int:
    similarity = 0

    for v1 in l1:
        similarity += d2[v1] * v1

    return similarity


@time_it
def main(data_lines: list[str]) -> None:
    l1, l2 = create_lists(data_lines)
    # print(l1)
    # print(l2)

    result = calc_similarity(l1, Counter(l2))

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 31
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 21070419
    #   Finished 'main' in 1 millisecond

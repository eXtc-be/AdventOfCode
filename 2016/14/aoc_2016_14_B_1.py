# aoc_2016_14_B_1.py - Day 14: One-Time Pad - part 2
# Given the actual salt in your puzzle input and using 2016 extra MD5 calls of key stretching,
# what index now produces your 64th one-time pad key?
# https://adventofcode.com/2016/day/14


from aoc_2016_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    CONSEC_1,
    CONSEC_2,
    NEXT,
    LIMIT,
    find_consecutive,
    check_consecutive,
)

from tools import time_it

import hashlib

from pprint import pprint

STRETCH = 2016

cache = {}


def get_stretched_hash(salt: str, index: int = 0, stretch: int = STRETCH) -> str:
    """returns the stretched MD5 hex digest of salt and index"""
    if index not in cache:
        hash = salt + str(index)
        for _ in range(stretch+1):
            hash = hashlib.md5(bytes(hash, 'ascii')).hexdigest()
        cache[index] = hash

    return cache[index]


@time_it
def main(data_lines: list[str]) -> None:
    keys = []
    i = 0
    while len(keys) < LIMIT:
        if c := find_consecutive(get_stretched_hash(data_lines[0], i), CONSEC_1):
            if any(check_consecutive(get_stretched_hash(data_lines[0], j), c, CONSEC_2) for j in range(i+1, i+1+NEXT)):
                # print(i)
                keys.append(i)
        i += 1

    print(f'End result: {keys[-1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 22551
    #   Finished 'main' in 46 seconds
    # using input data:
    #   End result: 22429
    #   Finished 'main' in 46 seconds

    # test stretched hash function
    # print(get_stretched_hash(data_lines[0], 0, STRETCH))

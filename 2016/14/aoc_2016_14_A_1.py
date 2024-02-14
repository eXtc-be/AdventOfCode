# aoc_2016_14_A_1.py - Day 14: One-Time Pad - part 1
# Given the actual salt in your puzzle input, what index produces your 64th one-time pad key?
# https://adventofcode.com/2016/day/14


from tools import time_it

import hashlib

from pprint import pprint


DATA_PATH = './input_2016_14'

CONSEC_1 = 3
CONSEC_2 = 5
NEXT = 1000
LIMIT = 64


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def find_consecutive(string: str, num: int) -> str:
    """returns the repeated character if string contains at least one substring of num identical characters"""
    for chars in zip(*[string[i:] for i in range(num)]):
        if len(set(chars)) == 1:
            return chars[0]


def check_consecutive(string: str, char: str, num: int) -> bool:
    """returns True if string contains at least one substring of num times char"""
    return char * num in string


cache = {}


def get_hash(salt: str, index: int = 0) -> str:
    """returns the MD5 hex digest of salt and index"""
    # hasher = hashlib.md5(bytes(salt + str(index), 'ascii'))
    # return hasher.hexdigest()
    if index not in cache:
        cache[index] = hashlib.md5(bytes(salt + str(index), 'ascii')).hexdigest()

    return cache[index]


test_data = '''
abc
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    keys = []
    i = 0
    while len(keys) < LIMIT:
        if c := find_consecutive(get_hash(data_lines[0], i), CONSEC_1):
            if any(check_consecutive(get_hash(data_lines[0], j), c, CONSEC_2) for j in range(i+1, i+1+NEXT)):
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
    #   End result: 22728
    #   Finished 'main' in 1.01 seconds
    # using input data:
    #   End result: 35186
    #   Finished 'main' in 1.57 seconds (5.5 seconds without caching)

    # test find_consecutive and check_consecutive
    # for test in [
    #     'abcdefghijklmnopqrst',
    #     'abcdeeehijklmnopqrst',
    #     'abcdefghijklmmmmpqrs',
    #     'abbcdefghijklmnopqrs',
    #     'abcdeeehijklmmmpqrst',
    #     'abcdefggggggmnopqrst',
    # ]:
    #     print(test, end=': ')
    #     if c := find_consecutive(test, 3):
    #         print(c, check_consecutive(test, c, 5))
    #     else:
    #         print('Nope')

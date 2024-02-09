# aoc_2016_05_A_1.py - Day 5: How About a Nice Game of Chess? - part 1
# Given the actual Door ID, what is the password?
# https://adventofcode.com/2016/day/5


from tools import time_it

import hashlib

from pprint import pprint


DATA_PATH = './input_2016_05'

THRESHOLD = 5

PASSWORD_LENGTH = 8


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def find_lowest_hash(secret: str, start: int = 0, threshold: int = THRESHOLD) -> tuple[int, str]:
    i = start
    while True:
        hasher = hashlib.md5(bytes(secret + str(i), 'ascii'))
        if hasher.hexdigest()[:threshold] == '0' * threshold:
            return i, hasher.hexdigest()
        i += 1


test_data = '''
abc
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # print(data_lines[0])

    password = ''
    index = 0

    for _ in range(PASSWORD_LENGTH):
        index, hex_digest = find_lowest_hash(data_lines[0], index+1, THRESHOLD)
        print(_, index, hex_digest)
        password += hex_digest[THRESHOLD]

    print(f'End result: {password}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 18f47a30
    #   Finished 'main' in 10 seconds
    # using input data:
    #   End result: f77a0e6e
    #   Finished 'main' in 10 seconds

    # test find_lowest_hash
    # first = find_lowest_hash(data_lines[0], 0, THRESHOLD)
    # print(first)


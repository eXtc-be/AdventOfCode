# aoc_2015_04_A_1.py - Day 4: The Ideal Stocking Stuffer - part 1
# Find the lowest positive number that produces a hash starting with 5 zeroes
# https://adventofcode.com/2015/day/4


from tools import time_it

import hashlib

from pprint import pprint


DATA_PATH = './input_2015_04'

THRESHOLD = 5


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def find_lowest_hash(secret: str, threshold: int = THRESHOLD) -> int:
    i = 0
    while True:
        hasher = hashlib.md5(bytes(secret + str(i), 'ascii'))
        if hasher.hexdigest()[:threshold] == '0' * threshold:
            return i
        i += 1


test_data = '''
abcdef
pqrstuv
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     result = find_lowest_hash(line)
    #     print(line, result)

    result = find_lowest_hash(data_lines[0])

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: 282749
    #   Finished 'main' in 1.05 seconds

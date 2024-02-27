# aoc_2017_14_A_1.py - Day 14: Disk Defragmentation - part 1
# Given your actual key string, how many squares are used?
# https://adventofcode.com/2017/day/14


from tools import time_it

import sys
sys.path.append(r'..\10')
from aoc_2017_10_B_1 import knothash

from pprint import pprint


DATA_PATH = './input_2017_14'

# HEX_TO_BITS = {
#     '0': 0,
#     '1': 1,
#     '2': 1,
#     '3': 2,
#     '4': 1,
#     '5': 2,
#     '6': 2,
#     '7': 3,
#     '8': 1,
#     '9': 2,
#     'a': 2,
#     'b': 3,
#     'c': 2,
#     'd': 3,
#     'e': 3,
#     'f': 4,
# }

HEX_TO_BITS = {
    '0': '....',
    '1': '...#',
    '2': '..#.',
    '3': '..##',
    '4': '.#..',
    '5': '.#.#',
    '6': '.##.',
    '7': '.###',
    '8': '#...',
    '9': '#..#',
    'a': '#.#.',
    'b': '#.##',
    'c': '##..',
    'd': '##.#',
    'e': '###.',
    'f': '####',
}

# HEX_TO_BITS = {
#     '0': '0000',
#     '1': '0001',
#     '2': '0010',
#     '3': '0011',
#     '4': '0100',
#     '5': '0101',
#     '6': '0110',
#     '7': '0111',
#     '8': '1000',
#     '9': '1001',
#     'a': '1010',
#     'b': '1011',
#     'c': '1100',
#     'd': '1101',
#     'e': '1110',
#     'f': '1111',
# }


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
flqrgnkx
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    total = 0
    for i in range(128):
        hex_hash = knothash(data_lines[0] + f'-{i}')
        # print(f'{hex_hash}')
        total += sum(HEX_TO_BITS[c] for c in hex_hash)
        # print(f'{sum(HEX_TO_BITS[c] for c in hex_hash)}')

    print(f'End result: {total}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 8108
    #   Finished 'main' in 1.59 seconds
    # using input data:
    #   End result: 8304
    #   Finished 'main' in 1.54 seconds

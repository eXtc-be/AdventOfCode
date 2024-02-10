# aoc_2016_09_A_1.py - Day 9: Explosives in Cyberspace - part 1
# What is the decompressed length of the file? Don't count whitespace.
# https://adventofcode.com/2016/day/9


from tools import time_it

import re

from pprint import pprint


DATA_PATH = './input_2016_09'

MARKER = re.compile(r'\(\d+x\d+\)')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def decompress(string: str) -> str:
    chars = string[:]  # deep copy
    result = ''

    while chars:
        if match := MARKER.search(chars):
            result += chars[:match.start()]  # add characters before the marker to the result
            num, repeat = match.group().strip('()').split('x')
            result += chars[match.end():match.end() + int(num)] * int(repeat)
            chars = chars[match.end() + int(num):]  # remove characters from chars
        else:  # no markers left in chars
            result += chars  # add the rest of the string to the result
            chars = ''

    return result


test_data = '''
ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     decompressed = decompress(line)
    #     print(f'{line} -> {decompressed} {len(decompressed)}')

    decompressed = decompress(data_lines[0])
    print(decompressed)

    print(f'End result: {len(decompressed)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 99145
    #   Finished 'main' in 5 milliseconds

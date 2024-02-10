# aoc_2016_09_B_1.py - Day 9: Explosives in Cyberspace - part 2
# What is the decompressed length of the file? Don't count whitespace.
# https://adventofcode.com/2016/day/9


from aoc_2016_09_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    MARKER,
)

from tools import time_it

import re

from pprint import pprint


# other constants


def decompress(string: str) -> str:
    chars = string[:]  # deep copy
    result = ''

    while chars:
        if match := MARKER.search(chars):
            result += chars[:match.start()]  # add characters before the marker to the result
            num, repeat = match.group().strip('()').split('x')
            slice = chars[match.end():match.end() + int(num)]
            result += decompress(slice) * int(repeat)
            chars = chars[match.end() + int(num):]  # remove characters from chars
        else:  # no markers left in chars
            result += chars  # add the rest of the string to the result
            chars = ''

    return result


test_data = '''
(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
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
    #   End result: 10943094568
    #   Finished 'main' in 17 seconds

# aoc_2015_08_A_1.py - Day 8: Matchsticks - part 1
# What is the number of characters of code for string literals
# minus the number of characters in memory
# for the values of the strings in total for the entire file?
# https://adventofcode.com/2015/day/8


from tools import time_it

import re

from pprint import pprint


DATA_PATH = './input_2015_08'

HEX_CHARS = '0123456789abcdef'

ESC_SLASH = '\\\\'
REP_SLASH = '\\'
ESC_QUOTE = '\\"'
REP_QUOTE = '"'
# ESC_HEX = re.compile(f'\\\\x')
ESC_HEX = re.compile(f'\\\\x[{HEX_CHARS}]{{2}}')

ASCII = 'ascii'


def load_data(path: str) -> list[str]:
    with open(path, 'r') as f:
        return f.read().splitlines()


def get_strings(data_lines: list[str]) -> list[str]:
    return [line.strip()[1:-1] for line in data_lines]


def decode_string(string: str) -> str:
    print(f'[{string}] -> ', end='')
    string = string.replace(ESC_SLASH, REP_SLASH)
    print(f'[{string}] -> ', end='')
    string = string.replace(ESC_QUOTE, REP_QUOTE)
    print(f'[{string}] -> ', end='')
    matches = ESC_HEX.findall(string)
    if matches:
        for match in matches:
            string = string.replace(match, chr(int(bytes(match, ASCII)[-2:].decode(ASCII), 16)))
    print(f'[{string}]')
    return string


@time_it
def main(data_lines: list[str]) -> None:
    strings = get_strings(data_lines)
    # print(strings)

    differences = []
    for string in strings:
        differences.append(len(string) - len(decode_string(string)))
    # print(differences)

    print(f'End result: {sum(differences) + 2 * len(differences)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = load_data('test_data')
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 1350
    #   Finished 'main' in 12 milliseconds

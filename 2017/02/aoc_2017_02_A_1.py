# aoc_2017_02_A_1.py - Day 2: Corruption Checksum - part 1
# What is the checksum for the spreadsheet in your puzzle input?
# https://adventofcode.com/2017/day/2


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_02'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_data(data_lines: list[str]) -> list[list[int]]:
    return [[int(v) for v in line.split()] for line in data_lines]


def checksum(data: list[list[int]]) -> int:
    return sum(max(row) - min(row) for row in data)


test_data = '''
5 1 9 5
7 5 3
2 4 6 8
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    data = get_data(data_lines)
    # print(data)

    print(f'End result: {checksum(data)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 18
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 47136
    #   Finished 'main' in less than a millisecond

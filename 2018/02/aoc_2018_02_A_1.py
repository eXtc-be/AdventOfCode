# aoc_2018_02_A_1.py - Day 2: Inventory Management System - part 1
# What is the checksum for your list of box IDs?
# https://adventofcode.com/2018/day/2
from collections import defaultdict

from tools import time_it

from collections import Counter

from pprint import pprint


DATA_PATH = './input_2018_02'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def check_id(id: str) -> tuple[int, int]:
    if len(set(id)) == len(id):
        return 0, 0

    counted = Counter(id)

    # print(counted)

    return (min(1, len([count for count in counted.values() if count == 2])),
            min(1, len([count for count in counted.values() if count == 3])))



test_data = '''
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    twos, threes = 0, 0

    for line in data_lines:
        two, three = check_id(line)
        # print(line, two, three)
        twos += two
        threes += three

    # print(twos, threes)

    print(f'End result: {twos * threes}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 12
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 5904
    #   Finished 'main' in 1 millisecond

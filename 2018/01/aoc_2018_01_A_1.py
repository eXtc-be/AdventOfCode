# aoc_2018_01_A_1.py - Day 1: Chronal Calibration - part 1
# Starting with a frequency of zero, what is the resulting frequency after all the changes have been applied?
# https://adventofcode.com/2018/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_01'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
+1
-2
+3
+1
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    freq = 0

    for line in data_lines:
        freq += int(line)

    print(f'End result: {freq}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 516
    #   Finished 'main' in less than a millisecond

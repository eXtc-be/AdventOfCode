# aoc_2015_10_A_1.py - Day 10: Elves Look, Elves Say - part 1
# Starting with the digits in your puzzle input, apply this process 40 times.  What is the length of the result?
# https://adventofcode.com/2015/day/10


from tools import time_it

from itertools import groupby

from pprint import pprint


DATA_PATH = './input_2015_10'

REPEATS = 50


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def look_and_say(string: str) -> str:
    # retval = ''
    #
    # for char, sequence in groupby(string):
    #     num = sum(1 for i in sequence)
    #     retval += str(num) + char
    #
    # return retval
    return ''.join(str(len(list(v))) + k for k, v in groupby(string))

test_data = '''
1
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    result = data_lines[0]
    # print(result.center(100))

    # for _ in range(10):
    for _ in range(REPEATS):
        result = look_and_say(result)
        # print(result.center(100))

    print(f'End result: {len(result)}')

    # with open('input_2015_10_2', 'w') as f:
    #     f.write(result)


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 492982
    #   Finished 'main' in 1.20 seconds
    #   Finished 'main' in 1 second with optimized look_and_say function

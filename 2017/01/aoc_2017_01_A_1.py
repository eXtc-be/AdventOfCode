# aoc_2017_01_A_1.py - Day 1: Inverse Captcha - part 1
# What is the solution to your captcha?
# https://adventofcode.com/2017/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_01'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_digits(digits: str) -> list[int]:
    return [int(d) for d in digits]


def check_digits(digits: list[int]) -> int:
    return sum(
        first
        for first, second in zip(digits, digits[1:]+digits[0:1])
        if first == second
    )


test_data = '''
1122
1111
1234
91212129
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     digits = get_digits(line)
    #     # print(digits)
    #
    #     result = check_digits(digits)
    #     print(result)

    print(f'End result: {check_digits(get_digits(data_lines[0]))}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3, 4, 0, 9
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1097
    #   Finished 'main' in 1 millisecond

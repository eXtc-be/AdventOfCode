# aoc_2017_01_B_1.py - Day 1: Inverse Captcha - part 2
# What is the solution to your captcha?
# https://adventofcode.com/2017/day/1


from aoc_2017_01_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_digits,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def check_digits(digits: list[int]) -> int:
    return sum(
        first
        for first, second in zip(digits[:len(digits)//2], digits[len(digits)//2:])
        if first == second
    ) * 2


test_data = '''
1212
1221
123425
123123
12131415
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     digits = get_digits(line)
    #     print(digits)
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
    #   End result: 6, 0, 4, 12, 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1188
    #   Finished 'main' in 1 millisecond

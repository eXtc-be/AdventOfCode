# aoc_2023_01_A_1.py - Day 1: Trebuchet?! - part 1
# Consider your entire calibration document. What is the sum of all the calibration values?
# https://adventofcode.com/2023/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_01'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_digits(data_lines: list[str]) -> list[list[str]]:
    return [[char for char in line if char.isdigit()] for line in data_lines]


def get_numbers(digits: list[list[str]]) -> list[int]:
    return [int(digit_list[0] + digit_list[-1]) for digit_list in digits]


test_data = '''
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    digits = get_digits(data_lines)
    # print(digits)

    numbers = get_numbers(digits)
    # print(numbers)

    print(f'End result: {sum(numbers)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 142
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 54708
    #   Finished 'main' in 1 millisecond

# aoc_2023_01_B_1.py - Day 1: Trebuchet?! - part 2
# What is the sum of all the calibration values with the new rules?
# https://adventofcode.com/2023/day/1


from aoc_2023_01_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_numbers,
)

from tools import time_it

# other imports

from pprint import pprint


NUMBER_STRINGS = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def get_digits(data_lines: list[str]) -> list[list[str]]:
    digits = []

    for line in data_lines:
        line_digits = []

        for i in range(len(line)):
            if line[i].isdigit():
                line_digits.append(line[i])
            else:
                for number_string, value in NUMBER_STRINGS.items():
                    if line[i:].startswith(number_string):
                        line_digits.append(str(value))
                        break

        digits.append(line_digits)

    return digits


test_data = '''
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
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
    #   End result: 281
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 54087
    #   Finished 'main' in 51 milliseconds

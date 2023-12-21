# aoc_01_A.py - Day 1: Trebuchet?! - part 1
# extract digits from lines of text, convert them to int and sum them
# https://adventofcode.com/2023/day/1


DATA_PATH = './input'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def get_digits(data):
    # numbers = []
    # for line in data:
    #     numbers.append(int(char) for char in line if char.isdigit())
    # return numbers
    return [[char for char in line if char.isdigit()] for line in data]


def get_numbers(digits):
    return [int(digit_list[0] + digit_list[-1]) for digit_list in digits]


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    digits = get_digits(data_lines)
    print(digits)

    numbers = get_numbers(digits)
    print(numbers)

    print(f'End result: {sum(numbers)}')

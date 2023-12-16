# aoc_01_A.py - Day 1: Trebuchet?! - part 2
# extract digits from lines of text, convert them to int and sum them - some numbers are now written out
# https://adventofcode.com/2023/day/1


data_path = 'input.txt'

number_strings = {
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


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def get_digits(data):
    return [[char for char in line if char.isdigit()] for line in data]


def get_digits_2(data):
    digits = []
    for line in data:
        line_digits = ''
        for i in range(len(line)):
            if line[i].isdigit():
                line_digits += line[i]
            else:
                for number_string, value in number_strings.items():
                    if line[i:].startswith(number_string):
                        line_digits += str(value)
                        break
        digits.append(line_digits)
    return digits


# def decode_written(data):
#     retval = []
#     for line in data:
#         for number_string, value in number_strings.items():
#             if number_string in line:
#                 line = line.replace(number_string, str(value))
#         retval.append(line)
#     return retval


def get_numbers(digits):
    return [int(digit_list[0] + digit_list[-1]) for digit_list in digits]


test_data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(data_path)
    # data_lines = test_data
    print(data_lines)

    digits = get_digits_2(data_lines)
    print(digits)

    numbers = get_numbers(digits)
    print(numbers)

    print(f'End result: {sum(numbers)}')

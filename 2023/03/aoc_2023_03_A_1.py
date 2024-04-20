# aoc_2023_03_A_1.py - Day 3: Gear Ratios - part 1
# find numbers that are adjacent to symbols
# https://adventofcode.com/2023/day/3


# imports


DATA_PATH = './input_2023_03'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def get_symbols(data):
    return set(char for line in data for char in line if not char.isdigit())


def _check_adjacent(data, i, j, number):
    left = j - len(number) - 1 if j - len(number) - 1 > 0 else 0
    right = j
    if data[i][left] in symbols or data[i][right] in symbols:
        return True
    else:
        above = data[i - 1] if i > 0 else ''
        below = data[i + 1] if i < len(data) - 1 else ''
    for line in above, below:
        if line:
            for idx in range(left, right + 1):
                if line[idx] in symbols:
                    return True


def find_numbers(data):
    """intermediate function to check if I got all numbers without doubles"""
    for i, line in enumerate(data):
        number = ''
        for j, char in enumerate(line):
            if char.isdigit():
                number += char
            else:
                if number:
                    yield int(number)
                    number = ''
        if number:  # check if a number was at the end of the line
            yield int(number)
            number = ''


def find_part_numbers(data):
    for i, line in enumerate(data):
        number = ''
        for j, char in enumerate(line):
            if char.isdigit():
                number += char
            else:
                if number:
                    if _check_adjacent(data, i, j, number):
                        yield int(number)
                    number = ''
        if number:  # check if a number was found at the end of the line
            if _check_adjacent(data, i, j, number):
                yield int(number)
            number = ''


test_data = """467..114..
...*......
..35..633.
......#...
617*......
.....+..58
..592.....
......755.
...$.*....
.664.598..""".splitlines()

if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    symbols = get_symbols(data_lines)
    symbols.discard(".")
    print(symbols)

    # numbers = list(find_numbers(data_lines))
    # print(numbers)
    # print(len(numbers))
    #
    # print(f'End result: {sum(numbers)}')

    numbers = list(find_part_numbers(data_lines))
    print(numbers)
    print(len(numbers))

    print(f'End result: {sum(numbers)}')

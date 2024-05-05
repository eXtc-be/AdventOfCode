# aoc_2023_03_A_1.py - Day 3: Gear Ratios - part 1
# What is the sum of all the part numbers in the engine schematic?
# https://adventofcode.com/2023/day/3


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_03'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_symbols(data_lines: list[str]) -> set[str]:
    return set(char for line in data_lines for char in line if not char.isdigit())


def _check_adjacent(data_lines: list[str], symbols: set[str], i: int, j: int, number_string: str):
    left = j - len(number_string) - 1 if j - len(number_string) - 1 > 0 else 0
    right = j

    if data_lines[i][left] in symbols or data_lines[i][right] in symbols:
        return True
    else:
        above = data_lines[i - 1] if i > 0 else ''
        below = data_lines[i + 1] if i < len(data_lines) - 1 else ''

        for line in above, below:
            if line:
                for idx in range(left, right + 1):
                    if line[idx] in symbols:
                        return True


def find_part_numbers(data_lines: list[str], symbols: set[str]):
    for i, line in enumerate(data_lines):
        number = ''
        j = None

        for j, char in enumerate(line):
            if char.isdigit():
                number += char
            else:
                if number:
                    if _check_adjacent(data_lines, symbols, i, j, number):
                        yield int(number)
                    number = ''

        if number:  # check if a number was found at the end of the line
            if _check_adjacent(data_lines, symbols, i, j, number):
                yield int(number)
            number = ''


test_data = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+..58
..592.....
......755.
...$.*....
.664.598..
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    symbols = get_symbols(data_lines)
    symbols.discard('.')  # Periods (.) do not count as a symbol.
    # print(symbols)

    numbers = list(find_part_numbers(data_lines, symbols))
    # print(numbers)
    # print(len(numbers))

    print(f'End result: {sum(numbers)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 4361
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 532428
    #   Finished 'main' in 4 milliseconds

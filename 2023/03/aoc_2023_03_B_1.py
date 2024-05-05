# aoc_2023_03_B_1.py - Day 3: Gear Ratios - part 2
# What is the sum of all of the gear ratios in your engine schematic?
# https://adventofcode.com/2023/day/3


from aoc_2023_03_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def _get_left(line: str, j: int) -> int:
    while j >= 0 and line[j].isdigit():
        j -= 1
    return j + 1


def _get_right(line: str, j: int) -> int:
    while j <= len(line)-1 and line[j].isdigit():
        j += 1
    return j


def _get_number(data_lines: list[str], i: int, j: int) -> int:
    left_idx = _get_left(data_lines[i], j)
    right_idx = _get_right(data_lines[i], j)
    return int(data_lines[i][left_idx:right_idx])


def _get_ratio_numbers(data_lines: list[str], i: int, j: int) -> list[int]:
    coords = []
    numbers = []

    # first find all adjacent cells with a digit in them
    if j > 0 and data_lines[i][j-1].isdigit():  # check if cell to the left has a number in it
        coords.append((i, j-1))

    if j+1 < len(data_lines[i]) - 1 and data_lines[i][j+1].isdigit():  # check if cell to the right has a number in it
        coords.append((i, j+1))

    if i > 0:
        if data_lines[i-1][j].isdigit():  # check if cell above has a number in it
            coords.append((i-1, j))
        else:  # if the cell above has a number, cells to the left or right belong to the same number
            if j > 0 and data_lines[i-1][j-1].isdigit():  # check if cell above and to the left has a number in it
                coords.append((i-1, j-1))
            if j+1 < len(data_lines[i-1]) - 1 and data_lines[i-1][j+1].isdigit():  # check if cell above and to the right has a number in it
                coords.append((i-1, j+1))

    if i < len(data_lines) - 1:
        if data_lines[i+1][j].isdigit():  # check if cell below has a number in it
            coords.append((i+1, j))
        else:  # if the cell below has a number, cells to the left or right belong to the same number
            if j > 0 and data_lines[i+1][j-1].isdigit():  # check if cell below and to the left has a number in it
                coords.append((i+1, j-1))
            if j+1 < len(data_lines[i+1]) - 1 and data_lines[i+1][j+1].isdigit():  # check if cell below and to the right has a number in it
                coords.append((i+1, j+1))

    # A gear is any * symbol that is adjacent to exactly two part numbers.
    if len(coords) == 2:
        for i, j in coords:
            numbers.append(_get_number(data_lines, i, j))
        return numbers
    # if more or less adjacent cell have a digit in them, just return a value that has no impact on the result
    else:
        return [0, 0]


def find_gears(data_lines: list[str]) -> list[list[int]]:
    for i, line in enumerate(data_lines):
        if '*' in line:
            for j in [p for p, char in enumerate(line) if char == '*']:
                yield _get_ratio_numbers(data_lines, i, j)


def calc_ratios(ratio_numbers: list[list[int]]) -> list[int]:
    return [num1 * num2 for num1, num2 in ratio_numbers]


@time_it
def main(data_lines: list[str]) -> None:
    ratio_numbers = list(find_gears(data_lines))
    # print(ratio_numbers)

    ratios = calc_ratios(ratio_numbers)
    # print(ratios)

    print(f'End result: {sum(ratios)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 467835
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 84051670
    #   Finished 'main' in 2 milliseconds

    # print(_get_number(test_data, 0, 2))  # 467
    # print(_get_number(test_data, 0, 6))  # 114

    # print(sum(line.count('*') for line in test_data))


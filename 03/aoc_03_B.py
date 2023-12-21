# aoc_03_B.py - Day 3: Gear Ratios - part 2
# find star symbols that are adjacent to exactly 2 numbers
# https://adventofcode.com/2023/day/3


from aoc_03_A import (
    DATA_PATH,
    load_data,
    test_data,
)


def _get_left(line, j):
    while j >= 0 and line[j].isdigit():
        j -= 1
    return j + 1


def _get_right(line, j):
    while j <= len(line)-1 and line[j].isdigit():
        j += 1
    return j


def _get_number(data, i, j):
    left = _get_left(data[i], j)
    right = _get_right(data[i], j)
    return int(data[i][left:right])


def _get_ratio_numbers(data, i, j):
    coords = []
    numbers = []

    # first find all adjacent cells with a digit in them
    if j > 0 and data[i][j-1].isdigit():  # check if cell to the left has a number in it
        coords.append((i, j-1))
    if j+1 < len(data[i]) - 1 and data[i][j+1].isdigit():  # check if cell to the right has a number in it
        coords.append((i, j+1))
    if i > 0:
        if data[i-1][j].isdigit():  # check if cell above has a number in it
            coords.append((i-1, j))
        else:
            if j > 0 and data[i-1][j-1].isdigit():  # check if cell above and to the left has a number in it
                coords.append((i-1, j-1))
            if j+1 < len(data[i-1]) - 1 and data[i-1][j+1].isdigit():  # check if cell above and to the right has a number in it
                coords.append((i-1, j+1))
    if i < len(data) - 1:
        if data[i+1][j].isdigit():  # check if cell below has a number in it
            coords.append((i+1, j))
        else:
            if j > 0 and data[i+1][j-1].isdigit():  # check if cell below and to the left has a number in it
                coords.append((i+1, j-1))
            if j+1 < len(data[i+1]) - 1 and data[i+1][j+1].isdigit():  # check if cell below and to the right has a number in it
                coords.append((i+1, j+1))

    # if exactly 2 adjacent cells have a digit in them, we can look for the full numbers
    if len(coords) == 2:
        for i, j in coords:
            numbers.append(_get_number(data, i, j))
        return numbers
    # if more or less adjacent cell have a digit in them, just return a value that has no impact on the result
    else:
        return [0, 0]


def find_gears(data):
    for i, line in enumerate(data):
        if '*' in line:
            for j in [p for p, char in enumerate(line) if char == '*']:
                yield _get_ratio_numbers(data, i, j)


def calc_ratios(ratio_numbers):
    return [num1 * num2 for num1, num2 in ratio_numbers]


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    # print(_get_number(data_lines, 0, 2))  # 467
    # print(_get_number(data_lines, 0, 6))  # 114

    stars = sum(line.count('*') for line in data_lines)
    print(stars)

    ratio_numbers = list(find_gears(data_lines))
    print(ratio_numbers)
    print(len([num for num in ratio_numbers if num != [0, 0]]))

    ratios = calc_ratios(ratio_numbers)
    print(ratios)
    print(len([ra for ra in ratios if ra != 0]))

    print(f'End result: {sum(ratios)}')

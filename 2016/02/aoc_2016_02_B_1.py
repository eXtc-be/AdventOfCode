# aoc_2016_02_B_1.py - Day 2: Bathroom Security - part 2
# What is the bathroom code?
# https://adventofcode.com/2016/day/2


from aoc_2016_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    Coordinates,
    DIRECTIONS,
    get_instructions,
)

from tools import time_it

# other imports

from pprint import pprint


KEYPAD = [
    [' ', ' ', '1', ' ', ' '],
    [' ', '2', '3', '4', ' '],
    ['5', '6', '7', '8', '9'],
    [' ', 'A', 'B', 'C', ' '],
    [' ', ' ', 'D', ' ', ' '],
]


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    instructions = get_instructions(data_lines)
    # pprint(instructions)

    code = ''
    min_row, max_row = 0, len(KEYPAD) - 1
    min_col, max_col = 0, len(KEYPAD[0]) - 1
    pos = Coordinates(0, 2)  # start position ('5')

    for line in instructions:
        for instruction in line:
            pos.x += DIRECTIONS[instruction].x
            pos.x = max(min_col, min(max_col, pos.x))
            if KEYPAD[pos.y][pos.x] == ' ':
                pos.x -= DIRECTIONS[instruction].x
            pos.y += DIRECTIONS[instruction].y
            pos.y = max(min_row, min(max_row, pos.y))
            if KEYPAD[pos.x][pos.y] == ' ':
                pos.y -= DIRECTIONS[instruction].y
        code += KEYPAD[pos.y][pos.x]

    print(f'End result: {code}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 5DB3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 8CB23
    #   Finished 'main' in 3 milliseconds

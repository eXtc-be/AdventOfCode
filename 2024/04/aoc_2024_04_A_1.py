# aoc_2024_04_A_1.py - Day 4: Ceres Search - part 1
# Take a look at the little Elf's word search. How many times does XMAS appear?
# https://adventofcode.com/2024/day/4


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2024_04'

# other constants

FIND = 'XMAS'

DIRECTIONS = (
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def count_words(data_lines: list[str]) -> int:
    total = 0

    for y, line in enumerate(data_lines):
        for x, char in enumerate(line):
            if data_lines[y][x] == FIND[0]:
                total += check_directions(data_lines, x, y)

    return total


def check_directions(data_lines: list[str], x: int, y: int) -> int:
    total = 0

    for dx,dy in DIRECTIONS:
        total += 1 if check_direction(data_lines, x, y, dx, dy) else 0

    return total


def check_direction(data_lines: list[str], x: int, y: int, dx: int, dy: int) -> bool:
    for i, l in enumerate(FIND[1:], 1):
        if y + dy * i < 0 or y + dy * i > len(data_lines) - 1:
            return False
        if x + dx * i < 0 or x + dx * i > len(data_lines[0]) - 1:
            return False
        if data_lines[y + dy * i][x + dx * i] != l:
            return False

    return True


test_data = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    result = count_words(data_lines)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 18
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 2462
    #   Finished 'main' in 28 milliseconds

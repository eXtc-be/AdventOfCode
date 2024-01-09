# aoc_2015_06_A_1.py - Day 6: Probably a Fire Hazard - part 1
# After following the instructions, how many lights are lit?
# https://adventofcode.com/2015/day/6


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_06'

GRID_SIZE = 1000
OFF = '.'
ON = '*'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def follow_instructions(instructions: list[str], grid: list[list[bool]]) -> None:
    for instruction in instructions:
        parts = instruction.split()
        if parts[0] == 'turn':
            x1, y1 = map(int, parts[2].split(','))
            x2, y2 = map(int, parts[4].split(','))

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if parts[1] == 'on':
                        grid[y][x] = True
                    else:
                        grid[y][x] = False
        elif parts[0] == 'toggle':
            x1, y1 = map(int, parts[1].split(','))
            x2, y2 = map(int, parts[3].split(','))

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    grid[y][x] = not grid[y][x]
        else:
            print(f'Invalid instruction: {instruction}')


test_data = '''
turn on 0,0 through 9,9
toggle 0,0 through 9,0
turn off 4,4 through 5,5
turn off 0,4 through 9,4
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    follow_instructions(data_lines, grid)

    # print('\n'.join(''.join(ON if char else OFF for char in row) for row in grid))

    print(f'End result: {sum(sum(1 if cell else 0 for cell in row) for row in grid)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 377891
    #   Finished 'main' in 1.45 seconds

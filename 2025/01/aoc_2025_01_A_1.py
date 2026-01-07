# aoc_2025_01_A_1.py - Day 1: Secret Entrance - part 1
# Analyze the rotations in your attached document. What's the actual password to open the door?
# https://adventofcode.com/2025/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2025_01'

# other constants
START = 50
DIAL = 100


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def process_rotations(lines: list[str]) -> int:
    current_position = START
    total_zeroes = 0

    for line in lines:
        direction = line[0]
        distance = int(line[1:])

        current_position = (current_position + distance if direction == 'R' else current_position - distance) % DIAL

        if current_position == 0:
            total_zeroes += 1

    return total_zeroes


test_data = '''
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    result = process_rotations(data_lines)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1129
    #   Finished 'main' in 1 millisecond

# aoc_2025_01_B_1.py - Day 1: Secret Entrance - part 2
# Using password method 0x434C49434B, what is the password to open the door?
# https://adventofcode.com/2025/day/1


from aoc_2025_01_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    START,
    DIAL,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions
def process_rotations(lines: list[str]) -> int:
    current_position = START
    total_zeroes = 0

    for line in lines:
        direction = line[0]
        distance = int(line[1:])

        total_zeroes += distance // DIAL
        distance -= (distance // DIAL) * DIAL

        if direction == 'R':
            if distance >= DIAL - current_position and current_position != 0:
                total_zeroes += 1
            current_position = (current_position + distance) % DIAL
        elif direction == 'L':
            if distance >= current_position and current_position != 0:
                total_zeroes += 1
            current_position = (current_position - distance) % DIAL
        else:
            raise ValueError(f'unknown direction: {direction}')

    return total_zeroes


@time_it
def main(data_lines: list[str]) -> None:
    result = process_rotations(data_lines)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 6638
    #   Finished 'main' in 2 milliseconds

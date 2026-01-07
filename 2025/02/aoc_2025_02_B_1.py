# aoc_2025_02_B_1.py - Day 2: Gift Shop - part 2
# What do you get if you add up all the invalid IDs using these new rules?
# https://adventofcode.com/2025/day/2


from aoc_2025_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions
def validate_range(start: int, end: int) -> int:
    return sum(number for number in range(start, end + 1) if is_invalid(number))


def is_invalid(number: int) -> bool:
    number_string = str(number)

    for divisor in range(2, len(number_string) + 1):
        if len(number_string) % divisor == 0:
            size = len(number_string) // divisor
            chunks = [number_string[pos:pos + size] for pos in range(0, len(number_string), size)]
            if all(chunk == chunks[0] for chunk in chunks[1:]):
                return True

    return False


@time_it
def main(data_line: str) -> None:
    result = 0

    for range_ in data_line.split(','):
        result += validate_range(*[int(val) for val in range_.split('-')])

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 4174379265
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 31578210022
    #   Finished 'main' in 5.2 seconds

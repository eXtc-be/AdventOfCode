# aoc_2025_02_A_1.py - Day 2: Gift Shop - part 1
# What do you get if you add up all the invalid IDs?
# https://adventofcode.com/2025/day/2


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2025_02'

# other constants


# classes


def load_data(path: str) -> str:
    with open(path) as f:
        return f.read()


# other functions
def validate_range(start: int, end: int) -> int:
    return sum(number for number in range(start, end + 1) if is_invalid(number))


def is_invalid(number: int) -> bool:
    number_string = str(number)
    if len(number_string) % 2 == 0:
        mid = len(number_string) // 2
        return number_string[:mid] == number_string[mid:]

    return False


test_data = ('11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,'
             '38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124')


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
    #   End result: 1227775554
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 28846518423
    #   Finished 'main' in 1 second

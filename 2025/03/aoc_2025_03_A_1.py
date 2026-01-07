# aoc_2025_03_A_1.py - Day 3: Lobby - part 1
# There are many batteries in front of you. Find the maximum joltage possible from each bank;
# what is the total output joltage?
# https://adventofcode.com/2025/day/3


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2025_03'

# other constants


# classes


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def get_max_jolt(bank: str) -> int:
    first_number = max(int(digit) for digit in bank[:-1])
    first_index = bank.index(str(first_number))
    second_number = max(int(digit) for digit in bank[first_index+1:])

    return 10 * first_number + second_number


test_data = '''
987654321111111
811111111111119
234234234234278
818181911112111
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    result = sum(get_max_jolt(line) for line in data_lines)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 357
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 17408
    #   Finished 'main' in 6 milliseconds

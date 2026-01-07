# aoc_2025_05_A_1.py - Day 5: Cafeteria - part 1
# Process the database file from the new inventory management system.
# How many of the available ingredient IDs are fresh?
# https://adventofcode.com/2025/day/5


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2025_05'

# other constants


# classes


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def create_range(ranges: list[str]) -> list[tuple[int, int]]:
    result = []

    for range_ in ranges:
        start, end = [int(v) for v in range_.split('-')]
        result.append((start, end+1))

    return result


def check_ingredient(ranges: list[tuple[int, int]], ingredient: int) -> bool:
    for range_ in ranges:
        if range_[0] < ingredient < range_[1]:
            return True

    return False


test_data = '''
3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    ranges = [line for line in data_lines if '-' in line]
    ingredients = [line for line in data_lines if '-' not in line and line]

    fresh = create_range(ranges)

    result = sum(1 if check_ingredient(fresh, int(ingredient)) else 0 for ingredient in ingredients)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 756
    #   Finished 'main' in 7 milliseconds

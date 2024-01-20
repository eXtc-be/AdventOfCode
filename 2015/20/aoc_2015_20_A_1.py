# aoc_2015_20_A_1.py - Day 20: Infinite Elves and Infinite Houses - part 1
# What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?
# https://adventofcode.com/2015/day/20


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_20'

FACTOR = 10


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _calc_house(house: int) -> int:
    result = 0

    for num in range(1, house + 1):
        if house % num == 0:
            result += num * FACTOR

    return result


def find_target_house(target: int) -> int:
    house = 1

    while True:
        value = _calc_house(house)
        if value >= target:
            break
        house += 1

    return house


test_data = '''
1_000_000
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    target = int(data_lines[0])

    result = find_target_house(target)

    print(f'End result: {result}: {_calc_house(result-1)} - {_calc_house(result)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data 1_000:
    #   End result: 48: 480 - 1240
    #   Finished 'main' in less than a millisecond
    # using test_data 10_000:
    #   End result: 360: 3600 - 11700
    #   Finished 'main' in 3 milliseconds
    # using test_data 100_000:
    #   End result: 3120: 31200 - 104160
    #   Finished 'main' in 273 milliseconds
    # using test_data 1_000_000:
    #   End result: 27720: 282960 - 1123200
    #   Finished 'main' in 22 seconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

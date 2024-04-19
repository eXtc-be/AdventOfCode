# aoc_2019_01_A_1.py - Day 1: The Tyranny of the Rocket Equation - part 1
# What is the sum of the fuel requirements for all the modules on your spacecraft?
# https://adventofcode.com/2019/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2019_01'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_masses(data_lines: list[str]) -> list[int]:
    return list(map(int, data_lines))


def get_fuel(masses: list[int]) -> list[int]:
    return [mass // 3 - 2 for mass in masses]


test_data = '''
12
14
1969
100756
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    masses = get_masses(data_lines)
    # pprint(masses)

    fuel = get_fuel(masses)
    # pprint(fuel)

    print(f'End result: {sum(fuel)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: [2, 2, 654, 33583] 34241
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 3336439
    #   Finished 'main' in less than a millisecond

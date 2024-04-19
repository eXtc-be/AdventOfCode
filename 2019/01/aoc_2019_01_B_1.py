# aoc_2019_01_B_1.py - Day 1: The Tyranny of the Rocket Equation - part 2
# What is the sum of the fuel requirements for all the modules on your spacecraft
# when also taking into account the mass of the added fuel?
# https://adventofcode.com/2019/day/1


from aoc_2019_01_A_1 import (
    DATA_PATH,
    load_data,
    get_masses,
    # test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def _calc_fuel(mass: int) -> int:
    return mass // 3 - 2 + _calc_fuel(mass // 3 - 2) if mass > 6 else 0


def get_fuel(masses: list[int]) -> list[int]:
    return [_calc_fuel(mass) for mass in masses]


test_data = '''
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
    #   End result: [2, 966, 50346] 51314
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 5001791
    #   Finished 'main' in less than a millisecond

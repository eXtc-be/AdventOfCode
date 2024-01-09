# aoc_2015_02_B_1.py - Day 2: I Was Told There Would Be No Math - part 2
# How many total feet of ribbon should they order?
# https://adventofcode.com/2015/day/2


from aoc_2015_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def calc_ribbon(dimensions: str) -> int:
    l, w, h = (int(d) for d in dimensions.split('x'))
    l1, l2 = sorted((l, w, h))[:2]
    return 2 * l1 + 2 * l2 + l * w *h


def calc_total_ribbon(data_lines: list[str]) -> int:
    return sum(calc_ribbon(line) for line in data_lines)


@time_it
def main(data_lines: list[str]) -> None:
    ribbon = calc_total_ribbon(data_lines)

    print(f'End result: {ribbon}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 3737498
    #   Finished 'main' in 3 milliseconds

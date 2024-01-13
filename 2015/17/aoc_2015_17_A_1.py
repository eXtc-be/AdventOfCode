# aoc_2015_17_A_1.py - Day 17: No Such Thing as Too Much - part 1
# Filling all containers entirely,
# how many different combinations of containers can exactly fit all 150 liters of eggnog?
# https://adventofcode.com/2015/day/17
from itertools import combinations

from tools import time_it

from itertools import combinations

from pprint import pprint


DATA_PATH = './input_2015_17'

TOTAL = 150


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_containers(data_lines: list[str]) -> list[int]:
    return [int(line) for line in data_lines]


def get_combos(containers: list[int]) -> list[list[int]]:
    combos = []

    for i in range(1, len(containers) + 1):
        combos += list(combinations(containers, i))

    return combos


test_data = '''
20
15
10
5
5 
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    containers = get_containers(data_lines)
    # print(containers)

    combos = get_combos(containers)
    # pprint(list(combos))

    good_combos = [combo for combo in combos if sum(combo) == TOTAL]
    # pprint(good_combos)

    print(f'End result: {len(good_combos)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1304
    #   Finished 'main' in 318 milliseconds

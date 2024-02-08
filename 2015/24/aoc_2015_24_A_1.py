# aoc_2015_24_A_1.py - Day 24: It Hangs in the Balance - part 1
# What is the quantum entanglement of the first group of packages in the ideal configuration?
# https://adventofcode.com/2015/day/24

import sys
sys.path.insert(0, '../..')

from tools import time_it

from itertools import combinations
from functools import reduce
from operator import mul

from pprint import pprint


DATA_PATH = './input_2015_24'

NUM_GROUPS = 3


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_packages(data_lines: list[str]) -> list[int]:
    return [int(line) for line in data_lines]


def quantum_entanglement(l: list[int]) -> int:
    return reduce(mul, l, 1)


test_data = '''
1
2
3
4
5
7
8
9
10
11
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], num_groups=NUM_GROUPS) -> None:
    candidates = []

    package_weights = get_packages(data_lines)
    print(f'{package_weights = }')

    total_weight = sum(package_weights)
    print(f'{total_weight = }')

    target_weight = total_weight // num_groups
    print(f'{target_weight = }')

    for length in range(1, len(package_weights)-(num_groups-1)):  # try every possible sublist length
        for combo in combinations(package_weights, r=length):  # try every combination of length=length
            if sum(combo) == target_weight:
                candidates.append(combo)

        print(f'{length = }; candidates = {candidates}')

        if candidates:
            break

    if candidates:
        candidates.sort(key=lambda c: (len(c), quantum_entanglement(c)))
        print(f'End result: {quantum_entanglement(candidates[0])}')
    else:
        print('Didn\'t find a solution.')



if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 99
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 11846773891
    #   Finished 'main' in 124 milliseconds

    # test quantum_entanglement
    # print(quantum_entanglement(list(range(1, 3))))  # 1*2=2
    # print(quantum_entanglement(list(range(1, 4))))  # 1*2*3=6
    # print(quantum_entanglement(list(range(1, 5))))  # 1*2*3*4=24

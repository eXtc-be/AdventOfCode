# aoc_2024_01_A_1.py - Day 1: Historian Hysteria - part 1
# What is the total distance between your lists?
# https://adventofcode.com/2024/day/1


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2024_01'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def create_lists(data_lines: list[str]) -> tuple[list[int], list[int]]:
    l1, l2 = [], []
    for line in data_lines:
        v1, v2 = [int(d) for d in line.split()]
        l1 += [v1]
        l2 += [v2]

    return l1, l2


def calc_distance(l1: list[int], l2: list[int]) -> int:
    distance = 0

    for v1, v2 in zip(sorted(l1), sorted(l2)):
        distance += abs(v1 - v2)

    return distance


test_data = '''
3   4
4   3
2   5
1   3
3   9
3   3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    l1, l2 = create_lists(data_lines)
    # print(l1)
    # print(l2)

    result = calc_distance(l1, l2)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 11
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1223326
    #   Finished 'main' in 1 millisecond

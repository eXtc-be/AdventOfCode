# aoc_2018_05_A_2.py - Day 5: Alchemical Reduction - part 1
# How many units remain after fully reacting the polymer you scanned?
# https://adventofcode.com/2018/day/5
# found on https://old.reddit.com/r/adventofcode/comments/d1matd/2018_day_5_part_1_helpcode_review_needed/fc6c48m/
# using a stack and only looping through all characters once


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_05'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def reduce(polymer: str) -> str:
    stack = []

    for unit in polymer:
        if stack and stack[-1] == unit.swapcase():
            stack.pop()
        else:
            stack.append(unit)

    return ''.join(stack)


test_data = '''
dabAcCaCBAcCcaDA
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    final = reduce(data)
    print(final)

    print(f'End result: {len(final)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # using test_data:
    #   End result: 10
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 11194
    #   Finished 'main' in 13 milliseconds

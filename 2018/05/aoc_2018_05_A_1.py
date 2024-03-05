# aoc_2018_05_A_1.py - Day 5: Alchemical Reduction - part 1
# How many units remain after fully reacting the polymer you scanned?
# https://adventofcode.com/2018/day/5


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_05'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def reduce(polymer: str) -> str:
    while True:
        # print(polymer)

        for i in range(len(polymer) - 1):
            if polymer[i].lower() == polymer[i+1] or polymer[i].upper() == polymer[i+1]:
                break
        else:  # no more reactions found
            return polymer

        polymer = polymer[:i] + polymer[i+2:]


test_data = '''
dabAcCaCBAcCcaDA
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    final = reduce(data)
    # print(final)

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
    #   End result: 10688 - too low
    #   Finished 'main' in 24 seconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

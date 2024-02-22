# aoc_2017_06_A_1.py - Day 6: Memory Reallocation - part 1
# How many redistribution cycles must be completed before a configuration is produced that has been seen before?
# https://adventofcode.com/2017/day/6


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_06'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_banks(banks: str) -> list[int]:
    return [int(bank) for bank in banks.split()]


def stringify(l: list[int]) -> str:
    return '_'.join(str(e) for e in l)


def redistribute_banks(banks: list[int]) -> list[str]:
    states = [stringify(banks)]
    # print(stringify(banks))
    num = 1

    while True:
        target = max([(b, i) for i, b in enumerate(banks)], key=lambda t: (t[0], -t[1]))

        banks[target[1]] = 0
        for i in range(target[0]):
            banks[(target[1] + 1 + i) % len(banks)] += 1

        # print(stringify(banks))
        if stringify(banks) in states:
            return states + [stringify(banks)]

        states.append(stringify(banks))
        num += 1



test_data = '''
0 2 7 0
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    banks = get_banks(data_lines[0])
    # print(banks)

    states = redistribute_banks(banks)
    print(states)

    print(f'End result: {len(states)-1}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 5
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 12841
    #   Finished 'main' in 226 milliseconds

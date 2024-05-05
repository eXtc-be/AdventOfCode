# aoc_2023_15_A_1.py - Day 15: Lens Library - part 1
# Run the HASH algorithm on each step in the initialization sequence. What is the sum of the results? (The initialization sequence is one long line; be careful when copy-pasting it.)
# https://adventofcode.com/2023/day/15


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_15'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def calculate_hash(text: str) -> int:
    hash = 0

    for c in text:
        hash += ord(c)
        hash *= 17
        hash %= 256

    return hash


test_data = ['rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7']


@time_it
def main(data_lines: list[str]) -> None:
    results = []

    for string in data_lines[0].split(','):
        result = calculate_hash(string)
        # print('the hash of {:10} is {:3}'.format(f'"{string}"', result))
        results.append((string, result))

    print(f'End result: {sum(result[1] for result in results)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 1320
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 512283
    #   Finished 'main' in 4 milliseconds

    # test calculate_hash
    # hash = calculate_hash('HASH')
    # print(hash)


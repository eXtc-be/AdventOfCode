# aoc_2017_21_B_1.py - Day 21: Fractal Art - part 2
# How many pixels stay on after 18 iterations?
# https://adventofcode.com/2017/day/21


from aoc_2017_21_A_1 import (
    DATA_PATH,
    START,
    load_data,
    test_data,
    enhance
)

from tools import time_it

# other imports

from pprint import pprint


ROUNDS = 18


# other functions


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    src = START
    dst = None

    for round in range(rounds):
        print(f'{round = }')

        # print('\n'.join(src))
        # print('-' * 100)

        dst = enhance(src, data_lines)
        # print('\n'.join(dst))
        # print('=' * 100)

        src = dst

    print(f'End result: {sum(row.count("#") for row in dst)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 2335049
    #   Finished 'main' in 54 seconds

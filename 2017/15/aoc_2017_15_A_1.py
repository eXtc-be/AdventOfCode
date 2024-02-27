# aoc_2017_15_A_1.py - Day 15: Dueling Generators - part 1
# After 40 million pairs, what is the judge's final count?
# https://adventofcode.com/2017/day/15


from tools import time_it

from typing import Generator

from pprint import pprint


DATA_PATH = './input_2017_15'

FACTOR_A = 16807
FACTOR_B = 48271

DIVISOR = 2147483647

BITS_TO_COMPARE = 16

ROUNDS = 40_000_000
ROUNDS_TEST = 5


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_start_values(data_lines: list[str]) -> tuple[int, ...]:
    return tuple(int(line.split()[-1]) for line in data_lines)


def generator_A(value: int) -> int:
    return value * FACTOR_A % DIVISOR


def generator_B(value: int) -> int:
    return value * FACTOR_B % DIVISOR


test_data = '''
Generator A starts with 65
Generator B starts with 8921
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    start_A, start_B = get_start_values(data_lines)
    # print(start_A, start_B)

    value_a = start_A
    value_b = start_B
    counter = 0
    for round in range(rounds):
        if round % 100_000 == 0:
            print(f'{round:,}')

        value_a = generator_A(value_a)
        value_b = generator_B(value_b)

        # bits_a = f'{value_a:032b}'[-BITS_TO_COMPARE:]
        # bits_b = f'{value_b:032b}'[-BITS_TO_COMPARE:]
        # print(f'{bits_a}\n{bits_b}\n')

        if value_a & (2 ** BITS_TO_COMPARE - 1) == value_b & (2 ** BITS_TO_COMPARE - 1):
            counter += 1

    print(f'End result: {counter}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, ROUNDS_TEST)
    # using test_data:
    #   End result: 588
    #   Finished 'main' in 40 seconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

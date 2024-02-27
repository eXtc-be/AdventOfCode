# aoc_2017_15_B_1.py - Day 15: Dueling Generators - part 2
# After 5 million pairs, but using this new generator logic, what is the judge's final count?
# https://adventofcode.com/2017/day/15


from aoc_2017_15_A_1 import (
    DATA_PATH,
    ROUNDS,
    ROUNDS_TEST,
    BITS_TO_COMPARE,
    load_data,
    test_data,
    get_start_values,
    generator_A,
    generator_B,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


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
        while value_a % 4:
            value_a = generator_A(value_a)
        value_b = generator_B(value_b)
        while value_b % 8:
            value_b = generator_B(value_b)

        # bits_a = f'{value_a:032b}'[-BITS_TO_COMPARE:]
        # bits_b = f'{value_b:032b}'[-BITS_TO_COMPARE:]
        # print(f'{value_a:13,} {bits_a}\n{value_b:13,} {bits_b}\n')

        if value_a & (2 ** BITS_TO_COMPARE - 1) == value_b & (2 ** BITS_TO_COMPARE - 1):
            counter += 1

    print(f'End result: {counter}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, 5_000_000)
    # main(data_lines, ROUNDS_TEST)
    # using test_data:
    #   End result: 309
    #   Finished 'main' in 21 seconds
    # using input data:
    #   End result: 298
    #   Finished 'main' in 20 seconds

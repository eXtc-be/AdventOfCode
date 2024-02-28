# aoc_2017_17_B_1.py - Day 17: Spinlock - part 2
# What is the value after 0 the moment 50000000 is inserted?
# https://adventofcode.com/2017/day/17


from aoc_2017_17_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


ROUNDS = 50_000_000


def do_spinlock(step: int, rounds: int = ROUNDS) -> int:
    length = 1
    value_at_1 = None
    pos = 0

    for round in range(1, rounds+1):
        if round % 1_000_000 == 0:
            print(f'{round:10,} {value_at_1}')

        pos = (pos + step) % length + 1
        length += 1
        if pos == 1:
            value_at_1 = round

    return value_at_1


@time_it
def main(data_lines: list[str]) -> None:
    step = int(data_lines[0])

    result = do_spinlock(step, ROUNDS)

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 31220910
    #   Finished 'main' in 14 seconds

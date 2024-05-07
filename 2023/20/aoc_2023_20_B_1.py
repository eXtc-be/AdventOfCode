# aoc_2023_20_B_1.py - Day 20: Pulse Propagation - part 2
# Consult your module configuration;
# determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times,
# waiting for all pulses to be fully handled after each push of the button.
# What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?
# https://adventofcode.com/2023/day/20


from aoc_2023_20_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    # your code

    print(f'End result: {0}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

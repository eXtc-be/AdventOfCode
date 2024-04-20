# aoc_2018_21_B_2.py - Day 21: Chronal Conversion - part 2
# What is the lowest non-negative integer value for register 0 that causes
# the program to halt after executing the most instructions?
# https://adventofcode.com/2018/day/21
# instead of interrupting the Elf program the first time it arrives at line 28, this program instead
# stores the value of register 5 in a list after verifying if it's not already in the list
# this version uses the Python translation of the Elf code program
# it runs a lot faster than executing the Elf code program, but it could be further optimized
# by replacing the inner loop (lines 17-27) by R3 //= 256 and by combining other lines


from aoc_2018_21_A_3 import (
    DATA_PATH,
    load_data,
    run_program,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    result = run_program(int(data_lines[8].split()[1]), repeat=True)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))

    # using input data:
    #   End result: 9547924
    #   Finished 'main' in 49 seconds

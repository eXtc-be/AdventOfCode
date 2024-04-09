# aoc_2018_21_B_1.py - Day 21: Chronal Conversion - part 2
# What is the lowest non-negative integer value for register 0 that causes
# the program to halt after executing the most instructions?
# https://adventofcode.com/2018/day/21
# instead of interrupting the Elf program the first time it arrives at line 28, this program instead
# stores the value of register 5 in a list after verifying if it's not already in the list
# this version is very slow: the first 10 values took 1 minute and 12 seconds to complete
# (the final result requires 10154 values to be calculated..)


from aoc_2018_21_A_1 import (
    DATA_PATH,
    Computer,
    Register,
    load_data,
    test_data,
    process_input,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    ip, program = process_input(data_lines)
    # print(ip)
    # pprint(program)

    computer = Computer(ip, [Register(i) for i in range(6)], program)

    computer.run(verbose=False, confirm=False, repeat=True)

    print(f'End result: {computer.registers[0].value}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))

    # using input data: not finished

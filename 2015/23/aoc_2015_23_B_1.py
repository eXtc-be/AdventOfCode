# aoc_2015_23_B_1.py - Day 23: Opening the Turing Lock - part 2
# What is the value in register b when the program in your puzzle input is finished executing?
# https://adventofcode.com/2015/day/23


from aoc_2015_23_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    read_program,
    Computer,
    Register
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    program = read_program(data_lines)
    # pprint(program)

    computer = Computer(
        [
            Register('a', 1),
            Register('b'),
        ],
        program
    )

    registers = computer.run_program()
    pprint(registers)

    print(f'End result: {registers[-1].value}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 231
    #   Finished 'main' in 1 millisecond

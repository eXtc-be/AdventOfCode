# aoc_2017_08_B_1.py - Day 8: I Heard You Like Registers - part 2
# What is the highest value held in any register while running the program?
# https://adventofcode.com/2017/day/8


from aoc_2017_08_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    Computer,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    computer = Computer()
    # pprint(computer)

    computer.read_program(data_lines)
    # pprint(computer.instructions)

    registers = computer.run_program()
    # print(registers)

    print(f'End result: {computer.highest}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 10
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 7234
    #   Finished 'main' in 7 milliseconds

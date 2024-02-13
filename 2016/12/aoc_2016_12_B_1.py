# aoc_2016_12_B_1.py - Day 12: Leonardo&apos;s Monorail - part 2
# After executing the assembunny code in your puzzle input, what value is left in register a?
# https://adventofcode.com/2016/day/12


from aoc_2016_12_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    read_program,
    Computer,
    Register,
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
            Register('a'),
            Register('b'),
            Register('c', 1),
            Register('d'),
        ],
        program
    )

    registers = computer.run_program()
    # pprint(registers)

    print(f'End result: {registers[0].value}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 42
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 9227661
    #   Finished 'main' in 21 seconds

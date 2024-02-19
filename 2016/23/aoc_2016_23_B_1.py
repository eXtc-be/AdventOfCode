# aoc_2016_23_B_1.py - Day 23: Safe Cracking - part 2
# What value should actually be sent to the safe?
# https://adventofcode.com/2016/day/23


from aoc_2016_23_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    Computer,
    Register,
    read_program,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


test_data = '''
cpy a b
dec b
cpy a d
cpy 0 a
cpy b c
inc a
dec c
jnz c -2
dec d
jnz d -5
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    program = read_program(data_lines)
    # pprint(program)

    computer = Computer(
        [
            Register('a', 12),
            Register('b'),
            Register('c'),
            Register('d'),
        ],
        program
    )

    registers = computer.run_program()
    pprint(registers)

    # print(f'End result: {registers[0].value}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: calculated by hand: 12 x 11 x .. x 3 x 2 + 76 x 84 = 479007984
    #   Finished 'main' in xxx

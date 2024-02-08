# aoc_2015_23_A_1.py - Day 23: Opening the Turing Lock - part 1
# What is the value in register b when the program in your puzzle input is finished executing?
# https://adventofcode.com/2015/day/23


from tools import time_it

from dataclasses import dataclass, field
from typing import Callable

from pprint import pprint


DATA_PATH = './input_2015_23'


@dataclass
class Register:
    name: str
    value: int = 0


@dataclass
class Instruction:
    function: str = ''
    register: str = ''
    offset: int = 0


@dataclass
class Computer:
    registers: list[Register]
    instructions: list[Instruction] = field(default_factory=list)
    program_counter: int = 0

    def run_program(self) -> list[Register]:
        while True:
            if 0 <= self.program_counter > len(self.instructions) - 1:
                break

            current_instruction = self.instructions[self.program_counter]

            if current_instruction.function not in INSTRUCTION_SET:
                break

            current_function_name = current_instruction.function
            current_register_name = current_instruction.register

            current_function_dict = INSTRUCTION_SET[current_function_name]

            current_function = current_function_dict['function']
            current_args = current_function_dict['args']

            current_register = None
            if 'register' in current_args:
                for register in self.registers:
                    if register.name == current_register_name:
                        current_register = register
                        break  # from inner for loop
                else:  # register not found
                    break  # from outer while loop

            current_offset = 0
            if 'offset' in current_args:
                current_offset = current_instruction.offset

            result = current_function(current_register, current_offset)

            if 'offset' in current_args:  # one of the jump functions
                self.program_counter += result
            else:
                self.program_counter += 1

        return self.registers


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def hlf(register: Register | None, offset: int = 0) -> int:
    register.value //= 2
    return 0


def tpl(register: Register | None, offset: int = 0) -> int:
    register.value *= 3
    return 0


def inc(register: Register | None, offset: int = 0) -> int:
    register.value += 1
    return 0


def jmp(register: Register | None, offset: int = 0) -> int:
    return offset


def jie(register: Register | None, offset: int = 0) -> int:
    if register.value % 2 == 0:
        return offset
    else:
        return 1


def jio(register: Register | None, offset: int = 0) -> int:
    if register.value == 1:
        return offset
    else:
        return 1


def read_program(data_lines: list[str]) -> list[Instruction]:
    instructions = []
    for line in data_lines:
        instruction = line[:3]
        register = ''
        offset = '0'
        if ',' in line[4:]:
            register, offset = line[4:].split(', ')
        else:
            if '+' in line[4:] or '-' in line[4:]:
                offset = line[4:]
            else:
                register = line[4:]
        offset = int(offset)
        instructions.append(Instruction(instruction, register, int(offset)))

    return instructions


INSTRUCTION_SET = {
    'hlf': {'function': hlf, 'args': ['register',]},
    'tpl': {'function': tpl, 'args': ['register',]},
    'inc': {'function': inc, 'args': ['register',]},
    'jmp': {'function': jmp, 'args': ['offset',]},
    'jie': {'function': jie, 'args': ['register', 'offset',]},
    'jio': {'function': jio, 'args': ['register', 'offset',]},
}


test_data = '''
inc a
jio a, +2
tpl a
inc a
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    program = read_program(data_lines)
    # pprint(program)

    computer = Computer(
        [
            Register('a'),
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
    #   End result: 184
    #   Finished 'main' in 1 millisecond

    # test Register class
    # register = Register('a')
    # pprint(register)

    # # test Instruction class
    # instruction = Instruction('inc', 'a')
    # pprint(instruction)

    # test Program class
    # program =[
    #     instruction,
    #     Instruction('tpl', register='a'),
    #     Instruction('jie', register='a', offset=2),
    #     Instruction('jmp', offset=-3),
    #     Instruction('hlf', register='a'),
    # ]
    # pprint(program)

    # test Computer class
    # computer = Computer(
    #     [Register('a')],
    #     instructions=program
    # )
    # pprint(computer)

    # registers = computer.run_program()
    # pprint(registers)

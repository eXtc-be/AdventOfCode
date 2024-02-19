# aoc_2016_23_A_1.py - Day 23: Safe Cracking - part 1
# What value should be sent to the safe?
# https://adventofcode.com/2016/day/23


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2016_23'

# other constants


@dataclass
class Register:
    name: str
    value: int = 0


@dataclass
class Instruction:
    function: str
    arg1: str | int
    arg2: str | int | None


@dataclass
class Computer:
    registers: list[Register]
    instructions: list[Instruction] = field(default_factory=list)
    program_counter: int = 0

    def run_program(self) -> list[Register]:
        while True:
            if not 0 <= self.program_counter < len(self.instructions):
                break  # quit if program jumps outside bounds

            current_instruction = self.instructions[self.program_counter]

            if current_instruction.function not in INSTRUCTION_SET:
                break  # quit if unknown instruction found

            current_function_name = current_instruction.function
            # current_src_name_value = current_instruction.arg1
            # current_dst_name = current_instruction.arg2

            current_function_dict = INSTRUCTION_SET[current_function_name]

            current_function = current_function_dict['function']
            # current_args = current_function_dict['args']

            current_arg1 = None
            if isinstance(current_instruction.arg1, int):
                current_arg1 = current_instruction.arg1
            elif isinstance(current_instruction.arg1, str):  # register
                for register in self.registers:
                    if register.name == current_instruction.arg1:
                        current_arg1 = register
                        break  # from inner for loop
                else:  # register not found
                    break  # from outer while loop

            current_arg2 = None
            if isinstance(current_instruction.arg2, int):
                current_arg2 = current_instruction.arg2
            elif isinstance(current_instruction.arg2, str):  # register
                for register in self.registers:
                    if register.name == current_instruction.arg2:
                        current_arg2 = register
                        break  # from inner for loop
                else:  # register not found
                    break  # from outer while loop

            result = current_function(current_arg1, current_arg2)

            if current_function_name == 'tgl':
                # check if target is within program bounds
                if 0 <= self.program_counter + result < len(self.instructions):
                    toggle(self.instructions[self.program_counter + result])

            if current_function_name == 'jnz':
                self.program_counter += result
            else:
                self.program_counter += 1

        return self.registers


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def cpy(src: Register | int, dst: Register) -> None:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src

    if isinstance(dst, Register):
        dst.value = value


def inc(dst: Register = None, src=None) -> None:
    if isinstance(dst, Register):
        dst.value += 1


def dec(dst: Register = None, src=None) -> None:
    if isinstance(dst, Register):
        dst.value -= 1


def jnz(src: Register | int, offset: Register | int) -> int:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src

    if value is not None and value != 0:
        if isinstance(offset, Register):
            return offset.value
        elif isinstance(offset, int):
            return offset
    else:
        return 1


def tgl(src: Register | int, dst=None, offset: int = 0) -> int:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src

    # return value and do the toggling in another function that has access to the computer's instructions
    return value


def toggle(instruction: Instruction) -> None:
    """in place replacement of instruction"""
    # change function
    instruction.function = INSTRUCTION_SET[instruction.function]['toggle']


def read_program(data_lines: list[str]) -> list[Instruction]:
    instructions = []
    for line in data_lines:
        arg1, arg2 = None, None

        parts = line.split()
        function = parts.pop(0)

        arg1 = parts.pop(0)
        if arg1.isdigit() or arg1.startswith('-'):
            arg1 = int(arg1)
        if parts:
            arg2 = parts.pop(0)
            if arg2.isdigit() or arg2.startswith('-'):
                arg2 = int(arg2)

        instructions.append(Instruction(function=function, arg1=arg1, arg2=arg2))

    return instructions


INSTRUCTION_SET = {
    'cpy': {'function': cpy, 'toggle': 'jnz'},
    'inc': {'function': inc, 'toggle': 'dec'},
    'dec': {'function': dec, 'toggle': 'inc'},
    'jnz': {'function': jnz, 'toggle': 'cpy'},
    'tgl': {'function': tgl, 'toggle': 'inc'},
}


test_data = '''
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    program = read_program(data_lines)
    # pprint(program)

    computer = Computer(
        [
            Register('a', 7),
            Register('b'),
            Register('c'),
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
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 11424
    #   Finished 'main' in 80 milliseconds

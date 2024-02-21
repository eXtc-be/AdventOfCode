# aoc_2016_25_A_1.py - Day 25: Clock Signal - part 1
# What is the lowest positive integer that can be used to initialize register a
# and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?
# https://adventofcode.com/2016/day/25


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2016_25'

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
            if current_function_name == 'brk':
                break

            current_function_dict = INSTRUCTION_SET[current_function_name]

            current_function = current_function_dict['function']

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


def tgl(src: Register | int, dst=None) -> int:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src

    # return value and do the toggling in another function that has access to the computer's instructions
    return value


def out(src: Register | int, dst=None) -> None:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src

    # return value and do the toggling in another function that has access to the computer's instructions
    print(f'OUT: {value}')


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

        if parts:
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
    'out': {'function': out, 'toggle': 'inc'},
    'brk': {'function': None, 'toggle': ''},
}


test_data = '''
cpy a d
cpy 7 c
cpy 365 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    program = read_program(data_lines)
    # pprint(program)

    computer = Computer(
        [
            Register('a', 175),
            Register('b'),
            Register('c'),
            Register('d'),
        ],
        program
    )

    registers = computer.run_program()
    pprint(registers)

    print(f'End result: {registers[0].value}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 175
    #   output pattern = binary representation of 7*365 + A
    #   1010 1010 1010 = 2730 -> 2730 - 2555 = 175

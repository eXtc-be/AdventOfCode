# aoc_2016_12_A_1.py - Day 12: Leonardo&apos;s Monorail - part 1
# After executing the assembunny code in your puzzle input, what value is left in register a?
# https://adventofcode.com/2016/day/12


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2016_12'

# other constants


@dataclass
class Register:
    name: str
    value: int = 0


@dataclass
class Instruction:
    function: str
    src: str | int
    dst: str | None
    offset: int | None


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
            current_src_name_value = current_instruction.src
            current_dst_name = current_instruction.dst

            current_function_dict = INSTRUCTION_SET[current_function_name]

            current_function = current_function_dict['function']
            current_args = current_function_dict['args']

            current_src = None
            current_src_args = current_args[0].split('|')
            if 'immediate' in current_src_args:
                if isinstance(current_src_name_value, int):
                    current_src = current_src_name_value
            if current_src is None and 'register' in current_src_args:
                for register in self.registers:
                    if register.name == current_src_name_value:
                        current_src = register
                        break  # from inner for loop
                else:  # register not found
                    break  # from outer while loop

            current_dst = None
            if current_args[1] == 'register':
                for register in self.registers:
                    if register.name == current_dst_name:
                        current_dst = register
                        break  # from inner for loop
                else:  # register not found
                    break  # from outer while loop

            current_offset = None
            if current_args[2] == 'offset':
                current_offset = current_instruction.offset

            result = current_function(current_src, current_dst, current_offset)

            if 'offset' in current_args:  # one of the jump functions
                self.program_counter += result
            else:
                self.program_counter += 1

        return self.registers


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def cpy(src: Register | int, dst: Register, offset=None) -> None:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src
    else:
        raise ValueError(f'Invalid source type: {type(src)}')
    dst.value = value
    return None


def inc(src=None, dst: Register = None, offset=None) -> None:
    dst.value += 1
    return None


def dec(src=None, dst: Register = None, offset=None) -> None:
    dst.value -= 1
    return None


def jnz(src: Register | int, dst=None, offset: int = 0) -> int:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src
    else:
        raise ValueError(f'Invalid source type: {type(src)}')

    if value is not None and value != 0:
        return offset
    else:
        return 1


def read_program(data_lines: list[str]) -> list[Instruction]:
    instructions = []
    for line in data_lines:
        src, dst, offset = None, None, None

        parts = line.split()
        function = parts.pop(0)

        match function:
            case 'cpy':
                src, dst = parts
                if src.isdigit():
                    src = int(src)
            case 'inc':
                dst = parts[0]
            case 'dec':
                dst = parts[0]
            case 'jnz':
                src, offset = parts
                if src.isdigit():
                    src = int(src)
                offset = int(offset)
            case _:
                raise ValueError(f'Invalid function: {function}')

        instructions.append(Instruction(function=function, src=src, dst=dst, offset=offset))

    return instructions


INSTRUCTION_SET = {
    'cpy': {'function': cpy, 'args': ['register|immediate', 'register', 'None',]},
    'inc': {'function': inc, 'args': ['None', 'register', 'None',]},
    'dec': {'function': dec, 'args': ['None', 'register', 'None',]},
    'jnz': {'function': jnz, 'args': ['register|immediate', 'None', 'offset',]},
}


test_data = '''
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    program = read_program(data_lines)
    # pprint(program)

    computer = Computer(
        [
            Register('a'),
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
    #   End result: 42
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 318007
    #   Finished 'main' in 1 second

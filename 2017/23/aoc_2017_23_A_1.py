# aoc_2017_23_A_1.py - Day 23: Coprocessor Conflagration - part 1
# If you run the program), how many times is the mul instruction invoked?
# https://adventofcode.com/2017/day/23


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2017_23'

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
    id: int = 0
    registers: list[Register] = field(default_factory=list)
    instructions: list[Instruction] = field(default_factory=list)
    program_counter: int = 0

    def read_program(self, data_lines: list[str]) -> None:
        for line in data_lines:
            arg1, arg2 = None, None

            parts = line.split()
            function = parts.pop(0)

            if parts:
                arg1 = parts.pop(0)
                if arg1.isdigit() or arg1.startswith('-'):
                    arg1 = int(arg1)
                elif arg1 not in [reg.name for reg in self.registers]:
                    self.registers.append(Register(arg1))
            if parts:
                arg2 = parts.pop(0)
                if arg2.isdigit() or arg2.startswith('-'):
                    arg2 = int(arg2)
                elif arg2 not in [reg.name for reg in self.registers]:
                    self.registers.append(Register(arg2))

            self.instructions.append(Instruction(function=function, arg1=arg1, arg2=arg2))

    def run_program(self) -> int:
        mul_counter = 0

        while True:
            if not 0 <= self.program_counter < len(self.instructions):
                break  # quit if program jumps outside bounds

            current_instruction = self.instructions[self.program_counter]

            if current_instruction.function not in INSTRUCTION_SET:
                break  # quit if instruction unknown

            current_function_name = current_instruction.function
            if current_function_name == 'brk':
                break

            if current_function_name == 'mul':
                mul_counter += 1

            current_function = INSTRUCTION_SET[current_function_name]

            current_arg1 = None
            if isinstance(current_instruction.arg1, int):
                current_arg1 = current_instruction.arg1
            elif isinstance(current_instruction.arg1, str):  # register
                for register in self.registers:
                    if register.name == current_instruction.arg1:
                        current_arg1 = register
                        break  # from inner for loop
                else:  # register not found -> quit program
                    break  # from outer while loop

            current_arg2 = None
            if isinstance(current_instruction.arg2, int):
                current_arg2 = current_instruction.arg2
            elif isinstance(current_instruction.arg2, str):  # register
                for register in self.registers:
                    if register.name == current_instruction.arg2:
                        current_arg2 = register
                        break  # from inner for loop
                else:  # register not found -> quit program
                    break  # from outer while loop

            result = current_function(current_arg1, current_arg2)

            if current_function_name == 'jnz':
                self.program_counter += result
            else:
                self.program_counter += 1

        return mul_counter


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _get_value(src: Register | int) -> int:
    value = None
    if isinstance(src, Register):
        value = src.value
    elif isinstance(src, int):
        value = src

    return value


def set(dst: Register, src: Register | int) -> None:
    dst.value = _get_value(src)


def sub(dst: Register, src: Register | int) -> None:
    dst.value -= _get_value(src)


def mul(dst: Register, src: Register | int) -> None:
    dst.value *= _get_value(src)


def jnz(src: Register | int, offset: Register | int) -> int:
    if _get_value(src) != 0:
        return _get_value(offset)
    else:
        return 1


INSTRUCTION_SET = {
    'set': set,
    'sub': sub,
    'mul': mul,
    'jnz': jnz,
    'brk': None,
}


@time_it
def main(data_lines: list[str]) -> None:
    computer = Computer()

    for reg in 'abcdefgh':
        computer.registers.append(Register(reg))
    # pprint(computer.registers)

    computer.read_program(data_lines)
    # pprint(computer.instructions)

    result = computer.run_program()
    # pprint(computer.registers)

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 9409
    #   Finished 'main' in 80 milliseconds

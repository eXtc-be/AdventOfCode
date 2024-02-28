# aoc_2017_18_A_1.py - Day 18: Duet - part 1
# What is the value of the recovered frequency (the value of the most recently played sound)
# the first time a rcv instruction is executed with a non-zero value?
# https://adventofcode.com/2017/day/18


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2017_18'

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
    last_played: int = field(default=None, init=False)

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
        while True:
            if not 0 <= self.program_counter < len(self.instructions):
                break  # quit if program jumps outside bounds

            current_instruction = self.instructions[self.program_counter]

            if current_instruction.function not in INSTRUCTION_SET:
                break  # quit if unknown instruction found

            current_function_name = current_instruction.function
            if current_function_name == 'brk':
                break

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

            if current_function_name == 'snd':
                self.last_played = result
                print(f'SND: {self.last_played}')
            elif current_function_name == 'rcv':
                if result:
                    print(f'RCV: {self.last_played}')
                    break

            if current_function_name == 'jgz':
                self.program_counter += result
            else:
                self.program_counter += 1

        return self.last_played


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


def snd(src: Register | int, dst=None) -> int:
    return _get_value(src)


def set(dst: Register, src: Register | int) -> None:
    dst.value = _get_value(src)


def add(dst: Register, src: Register | int) -> None:
    dst.value += _get_value(src)


def mul(dst: Register, src: Register | int) -> None:
    dst.value *= _get_value(src)


def mod(dst: Register, src: Register | int) -> None:
    dst.value %= _get_value(src)


def rcv(src: Register | int, dst=None) -> int:
    return _get_value(src)


def jgz(src: Register | int, offset: Register | int) -> int:
    if _get_value(src) > 0:
        return _get_value(offset)
    else:
        return 1


INSTRUCTION_SET = {
    'snd': snd,
    'set': set,
    'add': add,
    'mul': mul,
    'mod': mod,
    'rcv': rcv,
    'jgz': jgz,
    'brk': None,
}


test_data = '''
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    computer = Computer()

    computer.read_program(data_lines)
    # pprint(computer.instructions)
    # pprint(computer.registers)

    freq = computer.run_program()
    pprint(computer.registers)

    print(f'End result: {freq}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 7071
    #   Finished 'main' in 4 milliseconds

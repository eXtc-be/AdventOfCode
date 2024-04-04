# aoc_2018_19_A_1.py - Day 19: Go With The Flow - part 1
# What value is left in register 0 when the background process halts?
# https://adventofcode.com/2018/day/19
# main_alt_1 is the Elf code program translated to Python
# main_alt_2 is a slightly more efficient way of doing the same
# main_alt_3 is using a vastly more efficient way of calculating
#  the sum of all whole divisors of the number in register 3


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2018_19'

# other constants


@dataclass
class Register:
    id: int
    value: int = 0


@dataclass
class Instruction:
    name: str
    input_1: int
    input_2: int
    output: int


@dataclass
class Computer:
    ip: int
    registers: list[Register] = field(default_factory=list)
    program: list[Instruction] = field(default_factory=list)

    def run(self):
        while 0 <= self.registers[self.ip].value < len(self.program):
            instruction = self.program[self.registers[self.ip].value]

            if instruction.name and instruction.name in INSTRUCTION_SET:
                function_dict = INSTRUCTION_SET[instruction.name]
                fn = function_dict['fn']
                i1 = eval(function_dict['i1'])
                i2 = eval(function_dict['i2'])
                self.registers[instruction.output].value = fn(i1, i2)
            else:
                break

            self.registers[self.ip].value += 1


# instruction set functions
def add(input_1: int, input_2: int) -> int:
    return input_1 + input_2


def mul(input_1: int, input_2: int) -> int:
    return input_1 * input_2


def bor(input_1: int, input_2: int) -> int:
    return input_1 | input_2


def ban(input_1: int, input_2: int) -> int:
    return input_1 & input_2


def set_(input_1: int, input_2: int) -> int:
    return input_1


def eq(input_1: int, input_2: int) -> int:
    return int(input_1 == input_2)


def gt(input_1: int, input_2: int) -> int:
    return int(input_1 > input_2)


INSTRUCTION_SET = {
    'addr': {'fn': add,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'self.registers[instruction.input_2].value'},
    'addi': {'fn': add,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'instruction.input_2'},
    'mulr': {'fn': mul,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'self.registers[instruction.input_2].value'},
    'muli': {'fn': mul,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'instruction.input_2'},
    'borr': {'fn': bor,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'self.registers[instruction.input_2].value'},
    'bori': {'fn': bor,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'instruction.input_2'},
    'banr': {'fn': ban,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'self.registers[instruction.input_2].value'},
    'bani': {'fn': ban,  'i1': 'self.registers[instruction.input_1].value', 'i2': 'instruction.input_2'},
    'setr': {'fn': set_, 'i1': 'self.registers[instruction.input_1].value', 'i2': 'None'},
    'seti': {'fn': set_, 'i1': 'instruction.input_1',                       'i2': 'None'},
    'eqir': {'fn': eq,   'i1': 'instruction.input_1',                       'i2': 'self.registers[instruction.input_2].value'},
    'eqri': {'fn': eq,   'i1': 'self.registers[instruction.input_1].value', 'i2': 'instruction.input_2'},
    'eqrr': {'fn': eq,   'i1': 'self.registers[instruction.input_1].value', 'i2': 'self.registers[instruction.input_2].value'},
    'gtir': {'fn': gt,   'i1': 'instruction.input_1',                       'i2': 'self.registers[instruction.input_2].value'},
    'gtri': {'fn': gt,   'i1': 'self.registers[instruction.input_1].value', 'i2': 'instruction.input_2'},
    'gtrr': {'fn': gt,   'i1': 'self.registers[instruction.input_1].value', 'i2': 'self.registers[instruction.input_2].value'},
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def process_input(data_lines: list[str]) -> tuple[int, list[Instruction]]:
    ip = None
    program = []

    for line in data_lines:
        if line:
            if line.startswith('#ip'):
                ip = int(line.split()[-1])
            else:
                parts = line.split()
                program.append(Instruction(parts[0], *map(int, parts[1:])))

    return ip, program


test_data = '''
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    ip, program = process_input(data_lines)
    # print(ip)
    # pprint(program)

    computer = Computer(ip, [Register(i) for i in range(6)], program)

    computer.run()

    print(f'End result: {computer.registers[0].value}')


@time_it
def main_alt_1(hard: bool = False) -> None:
    r0 = 0
    r3 = 10551396 if hard else 996

    r1 = 1
    while r1 <= r3:
        r5 = 1
        while r5 <= r3:
            if r1 * r5 == r3:
                r0 += r1
            r5 += 1
        r1 += 1

    print(f'End result: {r0}')


@time_it
def main_alt_2(hard: bool = False) -> None:
    r0 = 0
    r3 = 10551396 if hard else 996

    for r1 in range(1, r3+1):
        for r5 in range(1, r3+1):
            if r1 * r5 == r3:
                r0 += r1

    print(f'End result: {r0}')


@time_it
def main_alt_3(hard: bool = False) -> None:
    r0 = 0
    r3 = 10551396 if hard else 996

    for r1 in range(1, r3+1):
        if r3 % r1 == 0:
            r0 += r1

    print(f'End result: {r0}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    # main(test_data)
    # main_alt_1()
    # main_alt_2()
    main_alt_3()

    # using test_data:
    #   End result: 7
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 2352
    #   Finished 'main' in 4 minutes and 14 seconds
    # using input data:
    #   End result: 2352
    #   Finished 'main_alt_1' in 102 milliseconds
    # using input data:
    #   End result: 2352
    #   Finished 'main_alt_2' in 48 milliseconds
    # using input data:
    #   End result: 2352
    #   Finished 'main_alt_3' in less than a millisecond

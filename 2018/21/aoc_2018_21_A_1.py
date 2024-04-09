# aoc_2018_21_A_1.py - Day 21: Chronal Conversion - part 1
# What is the lowest non-negative integer value for register 0 that causes
# the program to halt after executing the fewest instructions?
# https://adventofcode.com/2018/day/21
# this program just runs the Elf code until it arrives at line 28 (where register 0 is compared with register 5)
# then prints out the value of register 5 as the solution


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2018_21'

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


NUMBER_WIDTH = 18


@dataclass
class Computer:
    ip: int
    registers: list[Register] = field(default_factory=list)
    program: list[Instruction] = field(default_factory=list)

    @staticmethod
    def _process_mode(mode, value):
        if mode == 'r':
            return f"{f'R{value:,}':>{NUMBER_WIDTH}}"
        else:
            return f'{value:{NUMBER_WIDTH},}'

    def run(self, verbose: bool = False, confirm: bool = False, repeat: bool = False):
        numbers = []

        while 0 <= self.registers[self.ip].value < len(self.program):
            instruction = self.program[self.registers[self.ip].value]

            if verbose:
                input_1, input_2 = None, None
                match [letter for letter in instruction.name]:
                    case ['g', 't', mode_1, mode_2] | ['e', 'q', mode_1, mode_2]:
                        input_1 = self._process_mode(mode_1, instruction.input_1)
                        input_2 = self._process_mode(mode_2, instruction.input_2)
                    case ['s', 'e', 't', mode_1]:
                        input_1 = self._process_mode(mode_1, instruction.input_1)
                        input_2 = '*' * NUMBER_WIDTH
                    case [*_, mode_2]:
                        input_1 = f"{f'R{instruction.input_1:,}':>{NUMBER_WIDTH}}"
                        input_2 = self._process_mode(mode_2, instruction.input_2)

                registers = '[' + ' '.join([f'{register.value:{NUMBER_WIDTH},}' for register in self.registers]) + ']'
                # registers = '[' + ' '.join([f'R{register.id}={register.value:{NUMBER_WIDTH},}' for register in self.registers]) + ']'

                print(
                    f'{self.registers[self.ip].value:02}: '
                    f'{instruction.name} '
                    f'{input_1} '
                    f'{input_2} '
                    f'-> '
                    f'R{instruction.output} '
                    f'{registers}',
                    end=' '
                )
                if confirm:
                    input()
                else:
                    print()

            if self.registers[self.ip].value == 28:
                # this is the part where R0 is compared to R5 and the program halts if they are equal;
                # by returning the value of R5 at this point,
                # we get the value needed in R0 for the program to terminate
                if repeat:  # part 2
                    # for part 2 we need to find the value of R5 just before the sequence repeats
                    if len(numbers) % 1 == 0:
                        print(len(numbers), self.registers[5].value)
                    if self.registers[5].value in numbers:  # repeating value detected
                        self.registers[0].value = numbers[-1]  # store last value before loop in register 0
                        break
                    else:
                        numbers.append(self.registers[5].value)
                        if len(numbers) >= 10:
                            return numbers
                else:  # part 1
                    # for part 1 we only need the value of R5 the first time we arrive at line 28
                    break

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
#ip 2
seti 123 0 5
setr 3 0 5
eqir 1 2 3
eqri 4 5 0
gtrr 1 2 3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    ip, program = process_input(data_lines)
    # print(ip)
    # pprint(program)

    computer = Computer(ip, [Register(i) for i in range(6)], program)

    computer.run(verbose=True, confirm=False)
    # computer.run(verbose=False, confirm=False)

    print(f'End result: {computer.registers[5].value}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using input data:
    #   End result: 6619857
    #   Finished 'main' in 31 milliseconds

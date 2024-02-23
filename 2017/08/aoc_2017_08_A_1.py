# aoc_2017_08_A_1.py - Day 8: I Heard You Like Registers - part 1
# What is the largest value in any register after completing the program?
# https://adventofcode.com/2017/day/8


from tools import time_it

from dataclasses import dataclass, field
from typing import Callable
from operator import eq, ne, le, lt, ge, gt

from pprint import pprint


DATA_PATH = './input_2017_08'

# other constants


@dataclass
class Register:
    name: str
    value: int = 0


@dataclass
class Condition:
    source: Register
    op: Callable
    value: int

    def evaluate(self):
        return self.op(self.source.value, self.value)


@dataclass
class Instruction:
    destination: Register
    function: Callable
    amount: int
    condition: Condition

    def execute(self):
        if self.condition.evaluate():
            self.function(self.destination, self.amount)


@dataclass
class Computer:
    registers: list[Register] = field(default_factory=list)
    instructions: list[Instruction] = field(default_factory=list)
    highest: int = 0

    def read_program(self, datalines: list[str]):
        for line in datalines:
            dst, fun, am1, _, src, cmp, am2 = line.split()

            dst_reg = None
            for r in self.registers:
                if r.name == dst:
                    dst_reg = r
                    break
            else:  # not found -> create new register and add it
                dst_reg = Register(dst)
                self.registers.append(dst_reg)

            function = INSTRUCTION_SET[fun]

            amount1 = int(am1)

            src_reg = None
            for r in self.registers:
                if r.name == src:
                    src_reg = r
                    break
            else:  # not found -> create new register and add it
                src_reg = Register(src)
                self.registers.append(src_reg)

            op = OPERATORS[cmp]
            amount2 = int(am2)
            condition = Condition(src_reg, op, amount2)

            self.instructions.append(Instruction(dst_reg, function, amount1, condition))

    def run_program(self) -> list[Register]:
        for instruction in self.instructions:
            instruction.execute()
            self.highest = max(self.highest, max([reg.value for reg in self.registers]))

        return self.registers


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def inc(register: Register, amount: int) -> None:
    register.value += amount


def dec(register: Register, amount: int) -> None:
    register.value -= amount


INSTRUCTION_SET = {
    'inc': inc,
    'dec': dec,
}

OPERATORS = {
    '==': eq,
    '!=': ne,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge,
}


test_data = '''
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    computer = Computer()
    # pprint(computer)

    computer.read_program(data_lines)
    # pprint(computer.instructions)

    registers = computer.run_program()
    # print(registers)

    print(f'End result: {max(register.value for register in registers)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 1
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 6828
    #   Finished 'main' in 5 milliseconds

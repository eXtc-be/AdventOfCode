# aoc_2018_16_A_1.py - Day 16: Chronal Classification - part 1
# How many samples in your puzzle input behave like three or more opcodes?
# https://adventofcode.com/2018/day/16


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2018_16'

# other constants


@dataclass
class Register:
    id: int
    value: int = 0


@dataclass
class Instruction:
    opcode: int
    input_1: int
    input_2: int
    output: int
    name: str = ''


@dataclass
class Computer:
    registers: list[Register] = field(default_factory=list)
    program: list[Instruction] = field(default_factory=list)

    def run(self):
        for instruction in self.program:
            if instruction.name and instruction.name in INSTRUCTION_SET:
                function_dict = INSTRUCTION_SET[instruction.name]
                fn = function_dict['fn']
                i1 = eval(function_dict['i1'])
                i2 = eval(function_dict['i2'])
                self.registers[instruction.output].value = fn(i1, i2)


@dataclass
class Sample:
    before: list[int]
    instruction: Instruction
    after: list[int]


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


def process_input(data_lines: list[str]) -> tuple[list[Sample], list[Instruction]]:
    i = None
    test_cases = []
    for i, (before, code, after, _) in enumerate(zip(*[iter(data_lines)]*4)):
        if not before.startswith('Before'):  # end of test cases
            break

        test_cases.append(Sample(
            list(map(int, before[before.index('[')+1:before.index(']')].split(','))),
            Instruction(*map(int, code.split())),
            list(map(int, after[after.index('[')+1:after.index(']')].split(','))),
        ))

    program = []
    for line in data_lines[i*4:]:
        if line:
            program.append(Instruction(*map(int, line.split())))

    return test_cases, program


def evaluate_sample(sample: Sample) -> list[str]:
    result = []
    for instruction in INSTRUCTION_SET:
        sample.instruction.name = instruction
        computer = Computer(
            [Register(i, r) for i, r in enumerate(sample.before)],
            [sample.instruction]
        )
        computer.run()
        if [reg.value for reg in computer.registers] == sample.after:
            result.append(instruction)

    return result


def evaluate_samples(samples: list[Sample]) -> dict[int, list[str]]:
    results = {}

    for i, sample in enumerate(samples):
        results[i] = []
        for instruction_name in INSTRUCTION_SET:
            sample.instruction.name = instruction_name
            computer = Computer(
                [Register(i, r) for i, r in enumerate(sample.before)],
                [sample.instruction]
            )
            computer.run()
            if [reg.value for reg in computer.registers] == sample.after:
                results[i].append(instruction_name)

    return results


# test_data = '''
# Before: [0, 2, 1, 0]
# 3 0 0 1
# After:  [0, 0, 1, 0]
# // 13
# Before: [0, 1, 2, 1]
# 5 1 3 1
# After:  [0, 1, 2, 1]
# // 8
# // 15 out of 20 with count >= 3
# '''.strip().splitlines()

# test_data = '''
# Before: [3, 2, 1, 1]
# 9 2 1 2
# After:  [3, 2, 2, 1]
# // 3
# Before: [2, 1, 2, 3]
# 1 3 3 2
# After:  [2, 1, 3, 3]
# // 6
# Before: [2, 3, 2, 3]
# 14 3 2 3
# After:  [2, 3, 2, 2]
# // 2
# Before: [3, 3, 1, 1]
# 8 2 3 1
# After:  [3, 1, 1, 1]
# // 7
# Before: [0, 1, 0, 0]
# 0 3 1 3
# After:  [0, 1, 0, 1]
# // 5
# Before: [2, 1, 1, 2]
# 15 0 1 1
# After:  [2, 3, 1, 2]
# // 4
# Before: [0, 2, 2, 1]
# 15 0 2 1
# After:  [0, 2, 2, 1]
# // 4
# Before: [0, 2, 1, 0]
# 3 0 0 1
# After:  [0, 0, 1, 0]
# // 13
# Before: [3, 1, 2, 0]
# 0 3 1 2
# After:  [3, 1, 1, 0]
# // 5
# Before: [0, 1, 2, 1]
# 5 1 3 1
# After:  [0, 1, 2, 1]
# // 8
# Before: [2, 2, 2, 3]
# 11 3 3 1
# After:  [2, 9, 2, 3]
# // 2
# Before: [2, 1, 0, 3]
# 14 2 1 2
# After:  [2, 1, 1, 3]
# // 5
# Before: [0, 3, 2, 2]
# 4 0 2 0
# After:  [0, 3, 2, 2]
# // 12
# Before: [1, 0, 3, 3]
# 12 3 1 1
# After:  [1, 3, 3, 3]
# // 6
# Before: [0, 2, 3, 2]
# 7 2 3 3
# After:  [0, 2, 3, 2]
# // 2
# Before: [1, 1, 2, 3]
# 10 1 3 3
# After:  [1, 1, 2, 3]
# // 4
# Before: [2, 2, 2, 1]
# 6 3 2 1
# After:  [2, 3, 2, 1]
# // 5
# Before: [2, 1, 2, 0]
# 2 0 3 1
# After:  [2, 3, 2, 0]
# // 1
# Before: [1, 2, 3, 3]
# 11 2 3 1
# After:  [1, 9, 3, 3]
# // 2
# Before: [2, 1, 2, 2]
# 13 1 3 2
# After:  [2, 1, 3, 2]
# // 4
# // 15 out of 20 with count >= 3
# '''.strip().splitlines()

test_data = '''
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

Before: [2, 3, 3, 2]
11 2 0 2
After:  [2, 3, 1, 2]



5 2 0 2
10 2 0 2
15 3 2 3
15 2 3 0
6 3 2 3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    samples, program = process_input(data_lines)
    # pprint(samples)
    # pprint(program)

    results = evaluate_samples(samples)
    # pprint(results)

    qualified = {k: v for k, v in results.items() if len(v) >= 3}
    # pprint(qualified)

    print(f'End result: {len(qualified)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 1
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 677
    #   Finished 'main' in 487 milliseconds

    # test instructions
    # computer = Computer(
    #     [Register(i) for i in (range(4))],
    #     [
    #         Instruction(0, 0, 1, 0,  'addi'),  # r0 = r0 + 1   -> 1
    #         Instruction(0, 0, 0, 0,  'addr'),  # r0 = r0 + r0  -> 2
    #         Instruction(0, 0, 2, 1,  'muli'),  # r1 = r0 * 2   -> 4
    #         Instruction(0, 1, 1, 1,  'mulr'),  # r1 = r1 * r1  -> 16
    #         Instruction(0, 1, 5, 2,  'bori'),  # r2 = r1 | 5   -> 21
    #         Instruction(0, 2, 0, 2,  'borr'),  # r2 = r2 | r0  -> 23
    #         Instruction(0, 2, 29, 3, 'bani'),  # r3 = r2 | 29  -> 21
    #         Instruction(0, 3, 1, 3,  'banr'),  # r3 = r2 | r1  -> 16
    #         Instruction(0, 5, 0, 0,  'seti'),  # r0 = 5        -> 5
    #         Instruction(0, 2, 0, 1,  'setr'),  # r1 = r2       -> 23
    #         Instruction(0, 5, 0, 0,  'eqir'),  # r0 = 5 == r0  -> 1
    #         Instruction(0, 3, 16, 3, 'eqri'),  # r3 = r3 == 16 -> 1
    #         Instruction(0, 1, 2, 1,  'eqrr'),  # r1 = r1 == r2 -> 1
    #         Instruction(0, 5, 0, 2,  'gtir'),  # r2 = 5 > r0   -> 1
    #         Instruction(0, 0, 5, 0,  'gtri'),  # r0 = r0 > 5   -> 0
    #         Instruction(0, 0, 1, 1,  'gtrr'),  # r1 = r0 > r1  -> 0
    #     ]
    # )
    #
    # computer.run()
    # pprint(computer.registers)

    # # test evaluate_sample
    # for i, (before, code, after, expected) in enumerate(zip(*[iter(test_data)]*4)):
    #     if not before.startswith('Before'):  # end of test cases
    #         break
    #
    #     result = evaluate_sample(Sample(
    #         list(map(int, before[before.index('[')+1:before.index(']')].split(','))),
    #         Instruction(*map(int, code.split())),
    #         list(map(int, after[after.index('[')+1:after.index(']')].split(','))),
    #     ))
    #
    #     print(before)
    #     print(code)
    #     print(after)
    #     print(sorted(result), len(result), expected)
    #     print('-' * 100)

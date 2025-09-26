# aoc_2024_07_A_1.py - Day 7: Bridge Repair - part 1
# Determine which equations could possibly be true. What is their total calibration result?
# https://adventofcode.com/2024/day/7
from symtable import Class

from tools import time_it

# other imports

from pprint import pprint
from dataclasses import dataclass, field
from itertools import chain, zip_longest, product


OPERATORS = {
    '+': lambda n1, n2: n1 + n2,
    '*': lambda n1, n2: n1 * n2,
}


@dataclass
class Equation:
    result: int
    operands: list[int] = field(default_factory=list)
    operators: list[str] = field(default_factory=list)

    def _evaluate_(self) -> int:
        result = self.operands[0]
        for i, op in enumerate(self.operators):
            result = OPERATORS[op](result, self.operands[i + 1])
        return result

    def __bool__(self):
        return self.result == self._evaluate_()

    def __str__(self) -> str:
        if len(self.operators) == len(self.operands) - 1:
            return ' '.join(str(el) for el in chain.from_iterable(zip_longest(self.operands, self.operators)) if el)
            # return ' '.join(str(el) for el in zip(self.operands, self.operators)) + ' ' + str(self.operands[-1])
        else:
            return ''


DATA_PATH = './input_2024_07'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def create_equations(data_lines: list[str]) -> list[Equation]:
    equations = []

    for line in data_lines:
        result, operands = line.split(': ')
        result = int(result)
        operands = [int(operand) for operand in operands.split()]
        equations.append(Equation(result, operands))

    return equations


def solve_equation(equation: Equation) -> bool:
    for ops in product(OPERATORS, repeat=len(equation.operands) - 1):
        equation.operators = list(ops)
        if equation:
            return True

    return False


test_data = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # eq = Equation(230, [10, 20, 30])
    # print(eq)
    # print(eq._evaluate_())
    # print('yes' if eq else 'no')
    # print(solve_equation(eq))

    equations = create_equations(data_lines)
    # print(equations)
    result = sum(eq.result if solve_equation(eq) else 0 for eq in equations)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 3749
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1430271835320
    #   Finished 'main' in 433 milliseconds

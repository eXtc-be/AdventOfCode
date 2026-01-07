# aoc_2025_06_A_1.py - Day 6: Trash Compactor - part 1
# Solve the problems on the math worksheet. What is the grand total found by
# adding together all the answers to the individual problems?
# https://adventofcode.com/2025/day/6

from tools import time_it

# other imports

from pprint import pprint
from math import prod


DATA_PATH = './input_2025_06'

# other constants


# classes


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def get_problems(lines: list[str]) -> list[tuple]:
    numbers = [[int(val) if val.isdigit() else val for val in line.split()] for line in lines]

    return list(zip(*numbers))  # transpose XY matrix to YX matrix


def process_problem(problem: tuple) -> int:
    if problem[-1] == '+':
        return sum(problem[:-1])
    elif problem[-1] == '*':
        return prod(problem[:-1])
    else:
        raise ValueError(f'unknown operation: {problem[-1]}')


test_data = '''
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''.splitlines()[1:]


@time_it
def main(data_lines: list[str]) -> None:
    problems = get_problems(data_lines)

    result = sum(process_problem(problem) for problem in problems)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 4277556
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 6100348226985
    #   Finished 'main' in 2 milliseconds

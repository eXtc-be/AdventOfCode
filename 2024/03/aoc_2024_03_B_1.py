# aoc_2024_03_B_1.py - Day 3: Mull It Over - part 2
# Handle the new instructions; what do you get if you add up all the results of just the enabled multiplications?
# https://adventofcode.com/2024/day/3


from aoc_2024_03_A_1 import (
    DATA_PATH,
    load_data,
    calc,
)

from tools import time_it

# other imports

from pprint import pprint
from re import compile


# other constants

MUL = compile(r'''mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)''')


# other functions


test_data = '''mul(4*, mul(6,9!, ?(12,34)mul ( 2 , 4 )xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'''


@time_it
def main(data_lines: str) -> None:
    # print(MUL.findall(data_lines))

    result = 0
    enabled = True
    for exp in MUL.findall(data_lines):
        if exp.startswith('mul'):
            result += calc(exp) if enabled else 0
        elif exp.startswith("don't"):
            enabled = False
        elif exp.startswith('do'):
            enabled = True
        else:
            raise SyntaxError(f'unknown expression: {exp}')

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 48
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 93465710
    #   Finished 'main' in 1 millisecond

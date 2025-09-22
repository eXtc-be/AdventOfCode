# aoc_2024_03_A_1.py - Day 3: Mull It Over - part 1
# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all the results of the multiplications?
# https://adventofcode.com/2024/day/3


from tools import time_it

# other imports

from pprint import pprint
from re import compile


DATA_PATH = './input_2024_03'

# other constants

MUL = compile(r'mul\(\d{1,3},\d{1,3}\)')


def load_data(path: str) -> str:
    with open(path) as f:
        return ''.join(f.read().splitlines())


# other functions


def calc(exp: str) -> int:
    m1, m2 = [int(m) for m in exp[4:-1].split(',')]
    return m1 * m2


test_data = 'mul(4*, mul(6,9!, ?(12,34)mul ( 2 , 4 )xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'


@time_it
def main(data_lines: str) -> None:
    # print(MUL.findall(data_lines))

    result = sum(calc(exp) for exp in MUL.findall(data_lines))

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 161
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 166630675
    #   Finished 'main' in 1 millisecond

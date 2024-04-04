# aoc_2018_19_B_1.py - Day 19: Go With The Flow - part 2
# What value is left in register 0 when background process halts, starting with 1 in register 0?
# https://adventofcode.com/2018/day/19
# using the most efficient way from part 1, this program calculates the sum of all whole divisors
#  of a very large number
# to make this a more general solution we could execute the program and monitor the instruction pointer
#  until its value is equal to 1 (when the program returns from the subroutine that sets register 3)
#  and read the value of register 3, and then use that value in the optimized python program


from aoc_2018_19_A_1 import (
    DATA_PATH,
    load_data,
    Computer,
    Register,
    test_data,
    process_input,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(hard: bool = False) -> None:
    r0 = 0
    r3 = 10551396 if hard else 996

    for r1 in range(1, r3+1):
        if r3 % r1 == 0:
            r0 += r1

    print(f'End result: {r0}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using input data:
    #   End result: 24619952
    #   Finished 'main' in 1 second

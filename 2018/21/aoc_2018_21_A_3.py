# aoc_2018_21_A_2.py - Day 21: Chronal Conversion - part 1
# What is the lowest non-negative integer value for register 0 that causes
# the program to halt after executing the most instructions?
# https://adventofcode.com/2018/day/21
# this version replaces the inner loop (lines 17-27) by R3 //= 256 and does some other minor optimizations


from aoc_2018_21_A_1 import (
    DATA_PATH,
    load_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def run_program(param_1: int, repeat: bool = False) -> int:
    numbers = []

    # initialize registers
    R0, R1, R2, R3, R4, R5 = [0 for _ in range(6)]

    # we're skipping the part where the program tests the function of bani

    R5 = 0
    while True:
        R3 = R5 | 65536                 # 06 bori          R5       65536 -> R3
        R5 = param_1                    # 07 seti     9010242           x -> R5
        while True:
            R5 += R3 & 255
            R5 = R5 & 16777215          # 10 bani          R5    16777215 -> R5
            R5 = R5 * 65899             # 11 muli          R5       65899 -> R5
            R5 = R5 & 16777215          # 12 bani          R5    16777215 -> R5
            if 256 > R3:
                # this is the part where R0 is compared to R5 and the program halts if they are equal;
                # by returning the value of R5 at this point,
                # we get the value needed in R0 for the program to terminate
                if repeat:  # part 2
                    # for part 2 we need to find the value of R5 just before the sequence repeats
                    if len(numbers) % 1 == 0:
                        print(len(numbers), R5)
                    if R5 in numbers:  # repeating value detected
                        return numbers[-1]
                    else:
                        numbers.append(R5)
                        break
                else:  # part 1
                    # for part 1 we only need the value of R5 the first time we arraive at line 28
                    return R5
            else:
                R3 //= 256

@time_it
def main(data_lines: list[str]) -> None:
    result = run_program(int(data_lines[8].split()[1]))

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))

    # using input data:
    #   End result: 6619857
    #   Finished 'main' in less than a millisecond

# aoc_2017_23_B_1.py - Day 23: Coprocessor Conflagration - part 2
# After setting register a to 1, if the program were to run to completion, what value would be left in register h?
# https://adventofcode.com/2017/day/23
# the program does 1000 loops, incrementing b with 17 every loop, incrementing h if b is not a prime number
# because the numbers are so big, the program will run far too long, so this solution just
# counts the non-prime numbers between the start value of b and its end value, incrementing with 17


from aoc_2017_23_A_1 import (
    DATA_PATH,
    load_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def is_prime(n: int) -> bool:
    """https://stackoverflow.com/questions/15285534/isprime-function-for-python-language"""
    if n == 2 or n == 3: return True
    if n < 2 or n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False

    r = int(n ** 0.5)

    # since all primes > 3 are of the form 6n ± 1
    # start with f=5 (which is prime)
    # and test f, f+2 for being prime
    # then loop by 6.
    f = 5
    while f <= r:
        # print('\t', f)
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6

    return True


@time_it
def main(data_lines: list[str]) -> None:
    # first calculate the values of b, c and the increment
    b = int(data_lines[0].split()[-1])
    b *= int(data_lines[4].split()[-1])
    b -= int(data_lines[5].split()[-1])

    c = b - int(data_lines[7].split()[-1])

    i = -int(data_lines[-2].split()[-1])

    print(b, c, i)

    result = 0
    for num in range(b, c+1, i):
        if not is_prime(num):
            result += 1

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 913
    #   Finished 'main' in 1 millisecond

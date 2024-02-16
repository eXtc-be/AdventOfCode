# aoc_2016_19_B_2.py - Day 19: An Elephant Named Joseph - part 2
# With the number of Elves given in your puzzle input, which Elf gets all the presents with the new rules?
# https://adventofcode.com/2016/day/19
# strategy 2: using aoc_2016_19_B_1a.py to create a table of (number of elves, winner) pairs,
#   I discovered that w (the number of the winner), starting at 3^a, increments with 1
#   until n (the number of elves) is 2*3^a, after which w increments by 2 until the next
#   power of 3 is encountered, at which point the increments get back to 1
#   So, to calculate the winner instead of brute forcing it, we need to:
#       1. find the highest power of 3 (3^a) that is lower than the number of elves (n)
#       2. check if n is lower than twice the highest power of 3 (2 * 3^a) :
#           if yes, the winner is n - 3^a
#           if not, the winner is 3^a + 2 * (n - 2 * 3^a)


from aoc_2016_19_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

import math

from pprint import pprint


# other constants


def get_winner(num_elves: int) -> int:
    pass


@time_it
def main(num_elves: int) -> None:
    n1 = 3 ** int(math.log(num_elves, 3))  # get the largest power of 3 smaller than the number of elves
    n2 = 2 * n1

    if num_elves < n2:
        winner = num_elves - n1
    else:
        winner = n1 + (num_elves - n2) * 2

    print(f'End result: {winner}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    # main(57)
    main(int(data_lines[0]))
    # using input data:
    #   End result: 1417887
    #   Finished 'main' in less than a millisecond

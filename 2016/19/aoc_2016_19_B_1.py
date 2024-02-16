# aoc_2016_19_B_1.py - Day 19: An Elephant Named Joseph - part 2
# With the number of Elves given in your puzzle input, which Elf gets all the presents with the new rules?
# https://adventofcode.com/2016/day/19
# strategy 1: looping through all elves stealing presents until 1 elf has them all
#   using this strategy, the overhead of having all elves in memory is too large to be feasible


from aoc_2016_19_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def get_winner(num_elves: int) -> int:
    pass


@time_it
def main(num_elves: int) -> None:
    elves = {num: 1 for num in range(num_elves)}
    # print(elves)

    i = 0  # start next round with first surviving elf as thief
    while len(elves) > 1:
        p = list(elves.keys()).index(i)  # find thief elf's position in the remaining elves
        v = list(elves.keys())[(p + len(elves) // 2) % len(elves)]  # find next victim
        elves[i] += elves[v]
        del elves[v]
        i += 1
        while i not in elves.keys():  # find next thief
            if i > max(elves.keys()):
                i = 0
            else:
                i += 1

    print(f'End result: {list(elves.keys())[0] + 1}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(int(data_lines[0]))
    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: ???
    #   Finished 'main' in too long

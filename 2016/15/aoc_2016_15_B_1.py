# aoc_2016_15_B_1.py - Day 15: Timing is Everything - part 2
# What is the first time you can press the button to get a capsule with the extra disc?
# https://adventofcode.com/2016/day/15


from aoc_2016_15_A_1 import (
    DATA_PATH,
    load_data,
    test_data,get_discs,find_solution,Disc
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    discs = get_discs(data_lines)
    # pprint(discs)

    discs[len(discs)+1] = Disc(11, 0)
    # pprint(discs)

    solution = find_solution(discs)

    print(f'End result: {solution}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 85
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 3208099
    #   Finished 'main' in 2.6 seconds

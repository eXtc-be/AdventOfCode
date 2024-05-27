# aoc_2019_20_B_1.py - Day 20: Donut Maze - part 2
# In your maze, when accounting for recursion, how many steps does it take to get from the open tile marked AA
# to the open tile marked ZZ, both at the outermost layer?
# https://adventofcode.com/2019/day/20


from aoc_2019_20_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    # your code

    print(f'End result: {0}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

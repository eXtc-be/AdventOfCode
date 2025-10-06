# aoc_2024_11_B_1.py - Day 11: Plutonian Pebbles - part 2
# How many stones would you have after blinking a total of 75 times?
# https://adventofcode.com/2024/day/11

# stopped after 40 iterations, because this was getting too slow


from aoc_2024_11_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_stones,
    transform_stones,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_line: str) -> None:
    stones = get_stones(data_line)

    for i in range(75):
        stones = transform_stones(stones)

    print(f'End result: {len(stones)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

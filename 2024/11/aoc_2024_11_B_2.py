# aoc_2024_11_B_2.py - Day 11: Plutonian Pebbles - part 2
# How many stones would you have after blinking a total of 75 times?
# https://adventofcode.com/2024/day/11

# rewrote transform_stones to return the sum of the transformation of individual stones
# the function that calculates the number of stones for a given number of transformations is
# now recursive, which does not make it any faster by itself (in fact it's a tiny bit slower),
# but allows to use the @cache decorator from functools, which speeds up the process enormously


from aoc_2024_11_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_stones,
)

from tools import time_it

# other imports

from pprint import pprint
from functools import cache


# other constants


# other functions


@cache
def transform_stone(stone: int, amount: int) -> int:
    if amount == 0:
        return 1
    else:
        if stone == 0:
            return transform_stone(1, amount-1)
        elif len(s := str(stone)) % 2 == 0:
            return transform_stone(int(s[:(len(s) // 2)]), amount-1) + transform_stone(int(s[(len(s) // 2):]), amount-1)
        else:
            return transform_stone(stone * 2024, amount-1)


def transform_stones(stones: list[int], amount: int) -> int:
    return sum(transform_stone(stone, amount) for stone in stones)


@time_it
def main(data_line: str) -> None:
    stones = get_stones(data_line)

    result = transform_stones(stones, 75)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: 239321955280205
    #   Finished 'main' in 132 milliseconds

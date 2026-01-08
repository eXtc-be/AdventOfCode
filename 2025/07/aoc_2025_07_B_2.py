# aoc_2025_07_B_2.py - Day 7: Laboratories - part 2
# Apply the many-worlds interpretation of quantum tachyon splitting to your
# manifold diagram. In total, how many different timelines would a single
# tachyon particle end up on?
# https://adventofcode.com/2025/day/7

# attempt 2: multiplying the number of splits (minus 1 for some reason) by 2
# doesn't work, answer is higher than attempt 1 but still too low


from aoc_2025_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    split_beam,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    splits = split_beam(data_lines)

    print(f'End result: {(splits - 1) * 2}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 40
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 3394 -- too low
    #   Finished 'main' in 2 milliseconds

# aoc_2025_07_B_3.py - Day 7: Laboratories - part 2
# Apply the many-worlds interpretation of quantum tachyon splitting to your
# manifold diagram. In total, how many different timelines would a single
# tachyon particle end up on?
# https://adventofcode.com/2025/day/7

# attempt 3: recursively executing every timeline
# finds the correct answer in 3 milliseconds (after adding functools.cache and converting the list of lines to a tuple)


from aoc_2025_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint
from functools import cache


# other constants


# other functions
@cache
def split_beam(lines: tuple[str], line: int, pos: int) -> int:
    if line + 2 == len(lines):  # reached the end of the manifold
        return 1

    if lines[line + 2][pos] == '^':
        # splitter at beam's current position, split beam
        return split_beam(lines, line + 2, pos - 1) + split_beam(lines, line + 2, pos + 1)
    else:
        # no splitter at beam's current position, continue to the next line
        return split_beam(lines, line + 2, pos)


@time_it
def main(data_lines: list[str]) -> None:
    timelines = split_beam(tuple(data_lines), 0, data_lines[0].index('S'))

    print(f'End result: {timelines}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 40
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 95408386769474
    #   Finished 'main' in 3 milliseconds

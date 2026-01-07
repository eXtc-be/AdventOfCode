# aoc_2025_05_B_1.py - Day 5: Cafeteria - part 2
# Process the database file again.
# How many ingredient IDs are considered to be fresh according to the fresh ingredient ID ranges?
# https://adventofcode.com/2025/day/5

from aoc_2025_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_range,
)

from tools import time_it
from intervaltree import IntervalTree

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    ranges = [line for line in data_lines if '-' in line]

    fresh = create_range(ranges)
    # print(fresh)

    tree = IntervalTree.from_tuples(fresh)
    # print(tree)
    tree.merge_overlaps(strict=False)
    # print(tree)

    print(f'End result: {sum(el.end - el.begin for el in tree)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 14
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 355555479253787
    #   Finished 'main' in 3 milliseconds

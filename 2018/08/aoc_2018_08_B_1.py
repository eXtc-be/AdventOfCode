# aoc_2018_08_B_1.py - Day 8: Memory Maneuver - part 2
# What is the sum of all metadata entries?
# https://adventofcode.com/2018/day/8


from aoc_2018_08_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_definitions,
    parse,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    data = get_definitions(data_lines[0])
    # print(definitions)

    total, value, remaining = parse(data)
    # print(total, value, remaining)

    print(f'End result: {value}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 66
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 30857
    #   Finished 'main' in 122 milliseconds

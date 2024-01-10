# aoc_2015_07_B_1.py - Day 7: Some Assembly Required - part 2
# In little Bobby's kit's instructions booklet (provided as your puzzle input),
# what signal is ultimately provided to wire a?
# https://adventofcode.com/2015/day/7


from aoc_2015_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    WireList,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    wires = WireList()
    wires.get_wires(data_lines)
    wires['b'] = 46065  # override wire b with result from part 1

    print(f'End result: {wires.evaluate_wire(wires["a"])}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 14134
    #   Finished 'main' in 4 milliseconds

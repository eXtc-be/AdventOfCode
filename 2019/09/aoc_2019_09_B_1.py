# aoc_2019_09_B_1.py - Day 9: Sensor Boost - part 2
# Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?
# https://adventofcode.com/2019/day/9


from aoc_2019_09_A_1 import (
    DATA_PATH,
    Computer,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


INPUTS = [2]


# other functions


@time_it
def main(data: str, inputs: list[int] = INPUTS, verbose: bool = False, confirm: bool = False) -> None:
    computer = Computer(list(map(int, data.split(','))), inputs, verbose)
    # print(computer.memory)

    output = computer.run([], verbose, confirm)
    # output = computer.dump()
    # print(computer.memory)

    print(f'End result: {output}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0], INPUTS, False, False)
    # main(load_data(DATA_PATH)[0], INPUTS, True, False)
    # main(load_data(DATA_PATH)[0], INPUTS, True, True)

    # using input data:
    #   End result: 35106
    #   Finished 'main' in 2.1 seconds

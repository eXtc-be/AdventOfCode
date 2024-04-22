# aoc_2019_02_A_2.py - Day 2: 1202 Program Alarm - part 1
# What value is left at position 0 after the program halts?
# https://adventofcode.com/2019/day/2
# version using the Computer class from the intcode module


from aoc_2019_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

from intcode import Computer

from pprint import pprint


# other constants


# other functions


@time_it
def main(data: str) -> None:
    computer = Computer(list(map(int, data.split(','))))
    # print(computer.memory)

    computer.memory[1] = 12
    computer.memory[2] = 2

    computer.run()
    # print(computer.memory)

    print(f'End result: {computer.memory[0]}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])

    # using input data:
    #   End result: 3562672
    #   Finished 'main' in less than a millisecond

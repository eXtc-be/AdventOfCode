# aoc_2019_05_A_2.py - Day 5: Sunny with a Chance of Asteroids - part 1
# After providing 1 to the only input instruction and passing all the tests,
# what diagnostic code does the program produce?
# https://adventofcode.com/2019/day/5
# version using the Computer class from the intcode module


from aoc_2019_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

from intcode import Computer

from pprint import pprint


INPUT = 1

@time_it
def main(data: str) -> None:
    computer = Computer(list(map(int, data.split(','))), [INPUT])
    # print(computer.memory)

    output = computer.run()
    # print(computer.memory)

    print(f'End result: {output}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])

    # using input data:
    #   End result: 4601506
    #   Finished 'main' in 1 millisecond

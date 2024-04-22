# aoc_2019_02_B_2.py - Day 2: 1202 Program Alarm - part 2
# Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb?
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


OUTPUT = 19690720


# other functions


@time_it
def main(data: str) -> None:
    computer = None
    noun, verb = 0, 0

    for noun in range(100):
        # print(noun)
        for verb in range(100):
            # print('\t', verb)

            computer = Computer(list(map(int, data.split(','))))

            computer.memory[1] = noun
            computer.memory[2] = verb

            computer.run()

            # print('\t\t', computer.memory[0])

            if computer.memory[0] == OUTPUT:
                break

        if computer.memory[0] == OUTPUT:
            break

    print(f'End result: {100 * noun + verb}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])

    # using input data:
    #   End result: 8250
    #   Finished 'main' in 1.72 seconds

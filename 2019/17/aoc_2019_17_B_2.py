# aoc_2019_17_B_2.py - Day 17: Set and Forget - part 2
# After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?
# https://adventofcode.com/2019/day/17
# this program takes the scaffolding generator from aoc_2019_17_A_1, the path finding algorithm from aoc_2019_17_B_2a
# and the sequence divider from aoc_2019_17_B_2b and combines them into a complete solution


from aoc_2019_17_A_1 import (
    DATA_PATH,
    load_data,
    get_scaffolding_data,
    # test_data,
)

from aoc_2019_17_B_2a import (
    trace_path,
)

from aoc_2019_17_B_2b import (
    divide_sequence,
)

from tools import time_it

from intcode import Computer, State

from pprint import pprint


# other constants


# other functions


@time_it
def main() -> None:
    scaffolding_data = get_scaffolding_data()

    instructions = trace_path(scaffolding_data)

    main_func, func_A, func_B, func_C = divide_sequence(instructions)

    computer = Computer(list(map(int, load_data(DATA_PATH)[0].split(','))), [], False)
    # Force the vacuum robot to wake up by changing the value in your ASCII program at address 0 from 1 to 2.
    computer.memory[0] = 2

    computer.run([])  # run until first input command
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in main_func] + [10])
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in func_A] + [10])
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in func_B] + [10])
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in func_C] + [10])
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    computer.run([ord('n'), 10])  # answer 'n' when asked whether we want to see a continuous video feed
    # print(''.join([chr(char) for char in computer.outputs[:-1]]))

    print(f'End result: {computer.outputs[-1]}')


if __name__ == "__main__":
    main()

    # using input data:
    #   End result: 929045
    #   Finished 'main' in 1.74 seconds

# aoc_2019_17_B_1.py - Day 17: Set and Forget - part 2
# After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?
# https://adventofcode.com/2019/day/17
# this program only executes the intcode program with the main movement routine and the 3 movement functions
# I found those by annotating my scaffolding path (map.txt, map_w_instructions.txt) with the correct
# instructions (instructions.txt), then cutting up the instructions manually


from aoc_2019_17_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
)

from tools import time_it

from intcode import Computer, State

from pprint import pprint


INSTRUCTIONS = './instructions.txt'


# other functions


test_data = '''
R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2

A,B,C,B,A,C

A=R,8,R,8
B=R,4,R,4,R,8
C=L,6,L,2
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    computer = Computer(list(map(int, load_data(DATA_PATH)[0].split(','))), [], False)
    # Force the vacuum robot to wake up by changing the value in your ASCII program at address 0 from 1 to 2.
    computer.memory[0] = 2

    computer.run([])  # run until first input command
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in data_lines[2]] + [10])  # line 2 contains main movement routine
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in data_lines[4][2:]] + [10])  # line 4 contains movement function A
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in data_lines[5][2:]] + [10])  # line 5 contains movement function B
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    # continue program with input data
    computer.run([ord(char) for char in data_lines[6][2:]] + [10])  # line 6 contains movement function C
    # print(''.join([chr(char) for char in computer.outputs]))
    computer.outputs = []

    computer.run([ord('n'), 10])  # answer 'n' when asked whether we want to see a continuous video feed
    # print(''.join([chr(char) for char in computer.outputs[:-1]]))

    print(f'End result: {computer.outputs[-1]}')


if __name__ == "__main__":
    main(load_data(INSTRUCTIONS))
    # main(test_data)

    # using input data:
    #   End result: 929045
    #   Finished 'main' in 1.20 seconds

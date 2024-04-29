# aoc_2019_13_A_1.py - Day 13: Care Package - part 1
# Start the game. How many block tiles are on the screen when the game exits?
# https://adventofcode.com/2019/day/13


from tools import time_it
from intcode import Computer

# other imports

from pprint import pprint


DATA_PATH = './input_2019_13'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


@time_it
def main(data: str, verbose: bool = False, confirm: bool = False) -> None:
    computer = Computer(list(map(int, data.split(','))), [], verbose)

    computer.run()

    # take 3 output values at a time and count the ones where the third value equals the value for a block
    blocks = sum(1 for *_, t in zip(*[iter(computer.outputs)] * 3) if t == 2)

    print(f'End result: {blocks}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])

    # using input data:
    #   End result: 265
    #   Finished 'main' in 162 milliseconds

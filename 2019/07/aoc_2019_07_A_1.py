# aoc_2019_07_A_1.py - Day 7: Amplification Circuit - part 1
# What is the highest signal that can be sent to the thrusters?
# https://adventofcode.com/2019/day/7


from tools import time_it

from itertools import permutations

from intcode import Computer
from pprint import pprint


DATA_PATH = './input_2019_07'

INPUT = 0


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def calc_output(data: str, phases: tuple[int, ...], verbose: bool = False) -> int:
    value = INPUT
    program = list(map(int, data.split(',')))

    for i in range(len(phases)):
        computer = Computer(program, [phases[i], value], verbose)
        value = computer.run()

    return value


test_data = '''
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
'''.strip().splitlines()


@time_it
def main(data: str, verbose: bool = False) -> None:
    combos = {combo: calc_output(data, combo, verbose) for combo in permutations(range(5))}
    # pprint(combos)

    print(f'End result: {max(combos.values())}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # print(calc_output(test_data[0], (4, 3, 2, 1, 0)))
    # print(calc_output(test_data[1], (0, 1, 2, 3, 4)))
    # print(calc_output(test_data[2], (1, 0, 4, 3, 2)))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])

    # using test_data 0:
    #   End result: 43210
    #   Finished 'main' in 16 milliseconds
    # using test_data 1:
    #   End result: 54321
    #   Finished 'main' in 21 milliseconds
    # using test_data 2:
    #   End result: 65210
    #   Finished 'main' in 28 milliseconds
    # using input data:
    #   End result: 255840
    #   Finished 'main' in 29 milliseconds

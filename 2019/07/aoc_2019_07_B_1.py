# aoc_2019_07_B_1.py - Day 7: Amplification Circuit - part 2
# Try every combination of phase settings on the amplifiers.  What is the highest signal that can be sent to the thrusters?
# https://adventofcode.com/2019/day/7


from aoc_2019_07_A_1 import (
    DATA_PATH,
    INPUT,
    load_data,
    # test_data,
)

from intcode import Computer, State
from tools import time_it

from itertools import permutations

from pprint import pprint


# other constants


def calc_output(data: str, phases: tuple[int, ...], verbose: bool = False) -> int:
    value = INPUT

    computers = [Computer(list(map(int, data.split(','))), [phases[i]], verbose) for i in range(len(phases))]

    while not all(computer.state == State.halted for computer in computers):
        for computer in computers:
            if computer.state == State.paused:  # some computers may already have halted
                value = computer.run([value])

    return value


test_data = '''
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
'''.strip().splitlines()


@time_it
def main(data: str, verbose: bool = False) -> None:
    combos = {combo: calc_output(data, combo, verbose) for combo in permutations(range(5, 10))}
    # pprint(combos)

    print(f'End result: {max(combos.values())}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # print(calc_output(test_data[0], (9, 8, 7, 6, 5)))
    # print(calc_output(test_data[1], (9, 7, 8, 5, 6)))
    # main(test_data[0])
    # main(test_data[1])

    # using test_data 0:
    #   End result: 139629729
    #   Finished 'main' in 92 milliseconds
    # using test_data 1:
    #   End result: 18216
    #   Finished 'main' in 460 milliseconds
    # using input data:
    #   End result: 84088865
    #   Finished 'main' in 134 milliseconds

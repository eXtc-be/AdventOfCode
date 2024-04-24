# aoc_2019_09_A_1.py - Day 9: Sensor Boost - part 1
# What BOOST keycode does your Intcode computer produce?
# https://adventofcode.com/2019/day/9


from tools import time_it

from intcode import Computer

from pprint import pprint


DATA_PATH = './input_2019_09'

INPUTS = [1]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
1102,34915192,34915192,7,4,7,99,0
104,1125899906842624,99
'''.strip().splitlines()


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
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])

    # using test_data 0:
    #   End result: produces a copy of itself as output
    #   Finished 'main' in 1 millisecond
    # using test_data 1:
    #   End result: 1219070632396864
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 1125899906842624
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 2399197539
    #   Finished 'main' in 1 millisecond

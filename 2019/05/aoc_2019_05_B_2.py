# aoc_2019_05_B_2.py - Day 5: Sunny with a Chance of Asteroids - part 2
# What is the diagnostic code for system ID 5?
# https://adventofcode.com/2019/day/5


from aoc_2019_05_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
)

from tools import time_it

from intcode import Computer

from pprint import pprint


INPUT = 5


# other functions


test_data = '''
3,9,8,9,10,9,4,9,99,-1,8
3,9,7,9,10,9,4,9,99,-1,8
3,3,1108,-1,8,3,4,3,99
3,3,1107,-1,8,3,4,3,99
3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9
3,3,1105,-1,9,1101,0,0,12,4,12,99,1
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
'''.strip().splitlines()


@time_it
def main(data: str, input: int = INPUT) -> None:
    computer = Computer(list(map(int, data.split(','))), [input])
    # print(computer.memory)

    output = computer.run()
    # print(computer.memory)

    print(f'End result: {output}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], 7)
    # main(test_data[0], 8)
    # main(test_data[1], 7)
    # main(test_data[1], 8)
    # main(test_data[2], 7)
    # main(test_data[2], 8)
    # main(test_data[3], 7)
    # main(test_data[3], 8)
    # main(test_data[4], 0)
    # main(test_data[4], 123)
    # main(test_data[5], 0)
    # main(test_data[5], 123)
    # main(test_data[6], 7)
    # main(test_data[6], 8)
    # main(test_data[6], 9)

    # using input data:
    #   End result: 5525561
    #   Finished 'main' in 1 millisecond

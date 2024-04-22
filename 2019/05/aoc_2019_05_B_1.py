# aoc_2019_05_B_1.py - Day 5: Sunny with a Chance of Asteroids - part 2
# What is the diagnostic code for system ID 5?
# https://adventofcode.com/2019/day/5


from aoc_2019_05_A_1 import (
    DATA_PATH,
    load_data,
    get_program,
    run_program,
    # test_data,
)

from tools import time_it

# other imports

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
    program = get_program(data)
    # print(program)

    output = run_program(program, input)
    # print(program)

    print(f'End result: {output}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[6], 9)

    # using input data:
    #   End result: 5525561
    #   Finished 'main' in less than a millisecond

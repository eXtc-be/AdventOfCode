# aoc_2019_02_A_1.py - Day 2: 1202 Program Alarm - part 1
# What value is left at position 0 after the program halts?
# https://adventofcode.com/2019/day/2


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2019_02'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_program(data: str) -> list[int]:
    return list(map(int, data.split(',')))


def run_program(program: list[int]) -> None:
    pos = 0

    while True:
        match program[pos]:
            case 1:
                program[program[pos+3]] = program[program[pos+1]] + program[program[pos+2]]
            case 2:
                program[program[pos+3]] = program[program[pos+1]] * program[program[pos+2]]
            case 99:
                break
        pos += 4


test_data = '''
1,9,10,3,2,3,11,0,99,30,40,50
1,0,0,0,99
2,4,4,5,99,0
1,1,1,4,99,5,6,0,99
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    program = get_program(data)
    # print(program)

    # program[1] = 59
    # program[2] = 36
    program[1] = 12
    program[2] = 2

    run_program(program)
    # print(program)

    print(f'End result: {program[0]}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])

    # using input data:
    #   End result: 3562672
    #   Finished 'main' in less than a millisecond

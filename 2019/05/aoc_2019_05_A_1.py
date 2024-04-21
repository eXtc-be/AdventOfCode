# aoc_2019_05_A_1.py - Day 5: Sunny with a Chance of Asteroids - part 1
# After providing 1 to the only input instruction and passing all the tests,
# what diagnostic code does the program produce?
# https://adventofcode.com/2019/day/5


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2019_05'

INPUT = 1


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_program(data: str) -> list[int]:
    return list(map(int, data.split(',')))


def _get_param(program: list[int], pos: int, mode: int, num: int) -> int:
    if mode == 0:
        return program[program[pos+num]]
    else:
        return program[pos+num]


def run_program(program: list[int], input: int = INPUT) -> int:
    pos = 0
    last_output = None

    while True:
        instruction = f'{program[pos]:05}'
        opcode = int(instruction[-2:])
        mode_1 = int(instruction[2])
        mode_2 = int(instruction[1])
        mode_3 = int(instruction[0])
        match opcode:
            case 1:  # addition (3 parameters)
                assert mode_3 == 0  # Parameters that an instruction writes to will never be in immediate mode
                program[program[pos+3]] = _get_param(program, pos, mode_1, 1) + _get_param(program, pos, mode_2, 2)
                pos += 4
            case 2:  # multiplication (3 parameters)
                assert mode_3 == 0  # Parameters that an instruction writes to will never be in immediate mode
                program[program[pos+3]] = _get_param(program, pos, mode_1, 1) * _get_param(program, pos, mode_2, 2)
                pos += 4
            case 3:  # input (1 parameter)
                assert mode_1 == 0  # Parameters that an instruction writes to will never be in immediate mode
                program[program[pos+1]] = input
                pos += 2
            case 4:  # output (1 parameter)
                last_output = _get_param(program, pos, mode_1, 1)
                print(f'OUTPUT: {last_output}')
                pos += 2
            case 5:  # jump-if-true (2 parameters)
                if _get_param(program, pos, mode_1, 1) != 0:
                    pos = _get_param(program, pos, mode_2, 2)
                else:
                    pos += 3
            case 6:  # jump-if-false (2 parameters)
                if _get_param(program, pos, mode_1, 1) == 0:
                    pos = _get_param(program, pos, mode_2, 2)
                else:
                    pos += 3
            case 7:  # less than (3 parameters)
                assert mode_3 == 0  # Parameters that an instruction writes to will never be in immediate mode
                if _get_param(program, pos, mode_1, 1) < _get_param(program, pos, mode_2, 2):
                    program[program[pos + 3]] = 1
                else:
                    program[program[pos + 3]] = 0
                pos += 4
            case 8:  # equals (3 parameters)
                assert mode_3 == 0  # Parameters that an instruction writes to will never be in immediate mode
                if _get_param(program, pos, mode_1, 1) == _get_param(program, pos, mode_2, 2):
                    program[program[pos + 3]] = 1
                else:
                    program[program[pos + 3]] = 0
                pos += 4
            case 99:
                pos += 1
                return last_output


test_data = '''
1002,4,3,4,33
1101,100,-1,4,0
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    program = get_program(data)
    # print(program)

    output = run_program(program)
    # print(program)

    print(f'End result: {output}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[1])

    # using input data:
    #   End result: 4601506
    #   Finished 'main' in less than a millisecond

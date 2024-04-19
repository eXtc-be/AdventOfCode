# aoc_2019_02_B_1.py - Day 2: 1202 Program Alarm - part 2
# Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb?
# https://adventofcode.com/2019/day/2


from aoc_2019_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_program,
    run_program,
)

from tools import time_it

# other imports

from pprint import pprint


OUTPUT = 19690720


# other functions


@time_it
def main(data: str) -> None:
    program, noun, verb = 0, 0, 0

    for noun in range(100):
        # print(noun)
        for verb in range(100):
            # print('\t', verb)

            program = get_program(data)

            program[1] = noun
            program[2] = verb

            run_program(program)

            # print('\t\t', program[0])

            if program[0] == OUTPUT:
                break

        if program[0] == OUTPUT:
            break

    print(f'End result: {100 * noun + verb}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])

    # using input data:
    #   End result: 8250
    #   Finished 'main' in 1 second

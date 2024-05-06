# aoc_2019_17_B_2b.py - Day 17: Set and Forget - part 2
# After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?
# https://adventofcode.com/2019/day/17
# this program takes an instruction sequence to walk the path and tries all combinations to convert it to
# 1 main movement routine and the 3 movement functions, each part at most 20 characters long (including commas)


from aoc_2019_17_A_1 import (
    DATA_PATH,
    SCAFFOLD,
    EMPTY,
    HEADINGS,
    Coord,
    load_data,
    # test_data,
)

from tools import time_it

# other imports

from pprint import pprint


INSTRUCTIONS = './instructions.txt'


def divide_sequence(sequence: str) -> tuple[str, str, str, str] | None:
    # instruction sequence is of the form T,n,T,n,..
    #   where T: turn: 'L' or 'R'
    #         n: number of steps straight ahead
    # assumptions:
    #   function A always starts at the beginning of the sequence
    #   the smallest block we consider is T,n pair

    main_func = sequence[:]  # 'deep' copy
    func_A = ''
    func_B = ''
    func_C = ''

    start_A = 0
    end_A = start_A

    prev_A = main_func  # keep a copy of the main function in case we need to restore

    while True:
        end_A = main_func.find(',', end_A + 1)
        if end_A < 0 or main_func[end_A + 1] in 'A':
            break
        end_A = main_func.find(',', end_A + 1)
        if end_A < 0:
            break

        func_A = main_func[start_A:end_A]

        main_func = main_func.replace(func_A, 'A')

        # find the start of function B
        start_B = 0
        while main_func[start_B] in 'A,':
            start_B += 1
        end_B = start_B

        prev_B = main_func  # keep a copy of the main function in case we need to restore

        while True:
            end_B = main_func.find(',', end_B + 1)
            if end_B < 0 or main_func[end_B + 1] in 'AB':
                break
            end_B = main_func.find(',', end_B + 1)
            if end_B < 0:
                break

            func_B = main_func[start_B:end_B]

            main_func = main_func.replace(func_B, 'B')

            # find the start of function C
            start_C = 0
            while main_func[start_C] in 'AB,':
                start_C += 1
            end_C = start_C

            prev_C = main_func  # keep a copy of the main function in case we need to restore

            while True:
                end_C = main_func.find(',', end_C + 1)
                if end_C < 0 or main_func[end_C + 1] in 'ABC':
                    break
                end_C = main_func.find(',', end_C + 1)
                if end_C < 0:
                    break

                func_C = main_func[start_C:end_C]

                main_func = main_func.replace(func_C, 'C')

                # check whether we found a valid combo
                if (
                        all(char in 'ABC,' for char in main_func) and
                        all(len(part) <= 20 for part in (main_func, func_A, func_B, func_C))
                ):
                    return main_func, func_A, func_B, func_C

                main_func = prev_C  # restore main_func before retrying with next value

            main_func = prev_B  # restore main_func before retrying with next value

        main_func = prev_A # restore main_func before retrying with next value

    return None


test_data = '''
R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2

A,B,C,B,A,C

A=R,8,R,8
B=R,4,R,4,R,8
C=L,6,L,2
'''.strip().splitlines()


@time_it
def main(data: str) -> None:
    main_func, func_A, func_B, func_C = divide_sequence(data)

    print(f'End result: {main_func, func_A, func_B, func_C}')


if __name__ == "__main__":
    main(load_data(INSTRUCTIONS)[0])  # we could also get the instructions from aoc_2019_17_B_2, but this is (much) faster
    # main(load_data('./instructions_extern_1.txt')[0])
    # main(load_data('./instructions_extern_2.txt')[0])
    # main(test_data[0])

    # using test_data:
    #   End result: ('A,A,B,A,C,B,A,A,A,C', 'R,8', 'R,4,R,4', 'L,6,L,2')
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: ('A,A,B,C,B,A,C,B,C,A', 'L,6,R,12,L,6,L,8,L,8', 'L,6,R,12,R,8,L,8', 'L,4,L,4,L,6')
    #   Finished 'main' in 1 millisecond

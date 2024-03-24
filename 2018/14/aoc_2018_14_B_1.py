# aoc_2018_14_B_1.py - Day 14: Chocolate Charts - part 2
# How many recipes appear on the scoreboard to the left of the first recipes
# whose scores are the digits from your puzzle input?
# https://adventofcode.com/2018/day/14


from aoc_2018_14_A_1 import (
    DATA_PATH,
    load_data,
    START,
    # test_data,
    print_board,
    do_step,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


test_data = '''
51589
01245
92510
59414
'''.strip().splitlines()


@time_it
def main(data: str, verbose: bool = False) -> None:
    global steps_len

    board = [score for score in START]

    target = data

    elf_1 = 0
    elf_2 = 1

    if verbose:
        print_board(board, elf_1, elf_2)

    step = 1
    while ''.join(map(str, board[-len(target):])) != target:
        elf_1, elf_2 = do_step(board, elf_1, elf_2)
        if verbose:
            print_board(board, elf_1, elf_2, step)
        step += 1

    print(f'End result: {"".join(map(str, board)).index(target)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], verbose=True)
    # for line in test_data:
    #     print(line)
    #     main(line, verbose=False)

    # using test_data 51589:
    #   End result: 9
    #   Finished 'main' in less than a millisecond
    # using test_data 01245:
    #   End result: 5
    #   Finished 'main' in less than a millisecond
    # using test_data 92510:
    #   End result: 18
    #   Finished 'main' in less than a millisecond
    # using test_data 59414:
    #   End result: 2018
    #   Finished 'main' in 3 milliseconds
    # using input data:
    #   End result: 20322683
    #   Finished 'main' in 3 minutes and 23 seconds

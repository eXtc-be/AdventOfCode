# aoc_2016_21_B_1.py - Day 21: Scrambled Letters and Hash - part 2
# What is the result of scrambling abcdefgh?
# https://adventofcode.com/2016/day/21


from aoc_2016_21_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_new_password,
)

from tools import time_it

# other imports

from pprint import pprint


BASE_TEST = 'abdefghc'
BASE_REAL = 'fbgdceah'


# other functions


@time_it
def main(data_lines: list[str], password: str, verbose=False) -> None:
    new_password = get_new_password(data_lines, password, reverse=True)

    print(f'End result: {new_password}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    # main(data_lines, BASE_TEST, verbose=True)
    main(data_lines, BASE_REAL)
    # using test_data:
    #   End result: abcdefgh
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: bcfaegdh
    #   Finished 'main' in less than a millisecond

    # # test whether all reverse instructions work as intended
    # test = [c for c in 'abcdefgh']
    # # test = [c for c in 'abcde']
    # print(''.join(test))
    # from aoc_2016_21_A_1 import(
    #     _swap_positions,
    #     _swap_letters,
    #     _rotate_left,
    #     _rotate_right,
    #     _rotate,
    #     _reverse_positions,
    #     _move_positions,
    # )

    # # _swap_positions
    # _swap_positions(test, 2, 1)
    # print(''.join(test))
    # _swap_positions(test, 1, 2)
    # print(''.join(test))

    # # _swap_letters
    # _swap_letters(test, 'a', 'b')
    # print(''.join(test))
    # _swap_letters(test, 'b', 'a')
    # print(''.join(test))

    # # _rotate_left/_rotate_right
    # _rotate_left(test)
    # print(''.join(test))
    # _rotate_right(test)
    # print(''.join(test))

    # # _rotate
    # _rotate(test, 2)
    # print(''.join(test))
    # _rotate(test, -2)
    # print(''.join(test))

    # # _rotate_based
    # # test the logic in get_new_password for rotate based on position
    # instruction = 'rotate based on position of letter {l}'
    # for l in test:
    #     new = get_new_password([instruction.format(l=l)], test, reverse=False)
    #     new = get_new_password([instruction.format(l=l)], new, reverse=True)
    #     print('-' * 100)

    # # test _reverse_positions reverse=True
    # _reverse_positions(test, 1, 3)
    # print(''.join(test))
    # _reverse_positions(test, 3, 1)
    # print(''.join(test))

    # # test _move_positions reverse=True
    # _move_positions(test, 1, 4)
    # print(''.join(test))
    # _move_positions(test, 4, 1)
    # print(''.join(test))


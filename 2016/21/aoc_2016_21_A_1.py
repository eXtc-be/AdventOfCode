# aoc_2016_21_A_1.py - Day 21: Scrambled Letters and Hash - part 1
# What is the result of scrambling abcdefgh?
# https://adventofcode.com/2016/day/21


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2016_21'

BASE_TEST = 'abcde'
BASE_REAL = 'abcdefgh'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _swap_positions(password: list[str], pos_1: int, pos_2: int) -> None:
    password[pos_1], password[pos_2] = password[pos_2], password[pos_1]


def _swap_letters(password: list[str], letter_1: str, letter_2: str) -> None:
    _swap_positions(password, password.index(letter_1), password.index(letter_2))


def _rotate_left(password: list[str]) -> None:
    password[-1], password[:-1] = password[0], password[1:]


def _rotate_right(password: list[str]) -> None:
    password[0], password[1:] = password[-1], password[:-1]


def _rotate(password: list[str], steps: int) -> None:  # steps < 0 -> left; steps > 0 -> right
    for _ in range(abs(steps) % len(password)):
        _rotate_left(password) if steps < 0 else _rotate_right(password)


def _reverse_positions(password: list[str], pos_1: int, pos_2: int) -> None:
    password[min(pos_1, pos_2):max(pos_1, pos_2)+1] = password[min(pos_1, pos_2):max(pos_1, pos_2)+1][::-1]


def _move_positions(password: list[str], pos_1: int, pos_2: int) -> None:
    c = password.pop(pos_1)
    password.insert(pos_2, c)


def get_new_password(instructions: list[str], password: str, reverse: bool = False, verbose=False) -> str:
    # initialize new password as an array of letters (strings can't be changed in place)
    new_password = [c for c in password]
    if verbose:
        print(''.join(new_password))

    if reverse:
        instructions.reverse()

    for line in instructions:
        if verbose:
            print(f'{line}, {reverse=}')
        parts = line.split()
        match parts[0]:
            case 'swap':  # swap is NOT affected by reverse
                if parts[1] == 'position':
                    _swap_positions(new_password, int(parts[2]), int(parts[5]))
                elif parts[1] == 'letter':
                    _swap_letters(new_password, parts[2], parts[5])
            case 'rotate':  # rotate IS affected by reverse
                if parts[1] == 'left':  # left becomes right if reverse=True
                    _rotate(new_password, int(parts[2]) * (1 if reverse else -1))
                elif parts[1] == 'right':  # right becomes left if reverse=True
                    _rotate(new_password, int(parts[2]) * (-1 if reverse else 1))
                elif parts[1] == 'based':
                    if reverse:
                        idx = new_password.index(parts[6])
                        if idx == 0:
                            # idx = len(new_password)
                            idx = len(new_password) + len(new_password) % 2  # make it even
                        v = (idx+1) % 2  # 1 if even idx, 0 if odd idx
                        vv = v * (len(password)+1) // 2
                        idx = vv + 1 + idx // 2
                        _rotate(new_password, -idx)
                    else:
                        idx = new_password.index(parts[6])
                        idx += 1 + (idx // ((len(new_password)+1) // 2))
                        _rotate(new_password, idx)
            case 'reverse':  # reverse is NOT affected by reverse
                _reverse_positions(new_password, int(parts[2]), int(parts[4]))
            case 'move':  # move IS affected by reverse
                if reverse:
                    _move_positions(new_password, int(parts[5]), int(parts[2]))
                else:
                    _move_positions(new_password, int(parts[2]), int(parts[5]))
        if verbose:
            print(''.join(new_password))

    if verbose:
        print()
    return ''.join(new_password)


test_data = '''
swap position 7 with position 0
swap position 5 with position 2
swap letter g with letter b
swap letter d with letter e
reverse positions 0 through 7
rotate left 1 step
move position 1 to position 7
move position 6 to position 0
rotate based on position of letter b
rotate based on position of letter d
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], password: str, verbose=False) -> None:
    new_password = get_new_password(data_lines, password)

    print(f'End result: {new_password}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    # main(data_lines[0:2], BASE_TEST, verbose=True)
    # main(data_lines, BASE_TEST, verbose=True)
    main(data_lines, BASE_REAL)
    # using test_data:
    #   End result: decab
    #   Finished 'main' in less than a millisecond
    # using test_data and real base password:
    #   End result: abdefghc
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: gbhafcde
    #   Finished 'main' in less than a millisecond

    # # test instructions
    # test = [c for c in 'abcde']
    # print(''.join(test))

    # # test _swap_positions
    # _swap_positions(test, 1, 2)
    # print(''.join(test))
    # _swap_positions(test, 4, 0)
    # print(''.join(test))

    # # test _swap_letters
    # _swap_letters(test, 'a', 'b')
    # print(''.join(test))

    # # test _rotate_left
    # _rotate_left(test)
    # print(''.join(test))

    # # test _rotate_right
    # _rotate_right(test)
    # print(''.join(test))

    # # test _rotate
    # _rotate(test, -2)
    # print(''.join(test))
    # _rotate(test, 3)
    # print(''.join(test))

    # # test _rotate_based
    # idx = test.index('c')
    # idx += 1 + (1 if idx >= 4 else 0)
    # _rotate(test, idx)
    # print(''.join(test))
    # idx = test.index('b')
    # idx += 1 + (1 if idx >= 4 else 0)
    # _rotate(test, idx)
    # print(''.join(test))

    # # test _reverse_positions
    # _reverse_positions(test, 1, 3)
    # print(''.join(test))

    # # test _move_positions
    # _move_positions(test, 1, 4)
    # print(''.join(test))
    # _move_positions(test, 3, 0)
    # print(''.join(test))

# aoc_2015_11_A_1.py - Day 11: Corporate Policy - part 1
# Given Santa's current password, what should his next password be?
# https://adventofcode.com/2015/day/11


from tools import time_it

from itertools import groupby

from pprint import pprint


DATA_PATH = './input_2015_11'

EXCLUDED = tuple('iol')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _increment_last_char(pw: str) -> str:
    if pw[-1].lower() == 'z':
        if len(pw) == 1:
            return 'aa'
        return _increment_last_char(pw[:-1]) + 'a'
    else:
        return pw[:-1] + chr(ord(pw[-1]) + 1)


def _check_straight(pw: str) -> bool:
    if len(pw) >= 3:
        for x, y, z in zip(pw, pw[1:], pw[2:]):
            if ord(x)+2 == ord(y)+1 == ord(z):
                return True
    return False


def _check_excluded(pw: str, ex: str = EXCLUDED) -> bool:
    for c in pw:
        if c in ex:
            return False
    return True


def _check_pairs(pw: str) -> bool:
    return sum(1 for char, seq in groupby(pw) if len(list(seq)) >= 2) >= 2 if len(pw) >= 4 else False


def _validate_pw(pw: str) -> bool:
    # return _check_excluded(pw)
    # return _check_straight(pw)
    # return _check_pairs(pw)
    # return _check_excluded(pw) and _check_straight(pw)
    # return _check_excluded(pw)  and _check_pairs(pw)
    return _check_excluded(pw) and _check_straight(pw) and _check_pairs(pw)


def generate_new_pw(old: str) -> str:
    candidate = old
    while True:
        candidate = _increment_last_char(candidate)
        # print(candidate)
        if _validate_pw(candidate):
            return candidate


test_data = '''
xx
xy
xz
yz
abc
abb
ghh
abcaaba
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    new_pw = ''
    for line in data_lines:
        new_pw = generate_new_pw(line)
        # print(f'{line} -> {new_pw}')

    print(f'End result: {new_pw}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: hxbxxyzz
    #   Finished 'main' in 57 milliseconds

# aoc_2016_16_A_1.py - Day 16: Dragon Checksum - part 1
# The first disk you have to fill has length 272. Using the initial state in your puzzle input, what is the correct checksum?
# https://adventofcode.com/2016/day/16


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2016_16'

LIMIT_REAL = 272
LIMIT_TEST = 20


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _invert(bits: str) -> str:
    return ''.join('1' if bit == '0' else '0' for bit in bits)


def _reverse(bits: str) -> str:
    return bits[::-1]


def dragon_step(bits: str) -> str:
    return bits + '0' + _invert(_reverse(bits))


def do_dragon(bits: str, limit: int) -> str:
    result = bits
    while len(result) < limit:
        result = dragon_step(result)
    return result


def _checksum(bits: str) -> str:
    result = ''
    for pair in zip(bits[::2], bits[1::2]):
        result += '1' if pair[0] == pair[1] else '0'
    return result


def checksum(bits: str) -> str:
    result = bits
    while len(result) % 2 == 0:
        result = _checksum(result)
    return result


test_data = '''
10000
'''.strip().splitlines()


@time_it
def main(initial: str, limit: int) -> None:
    d = do_dragon(initial, limit)
    print(initial)
    print(d)
    print(checksum(d[:limit]))

    print(f'End result: {checksum(d[:limit])}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    limit = LIMIT_REAL
    # limit = LIMIT_TEST
    # print(data_lines)

    main(data_lines[0], limit)
    # using test_data:
    #   End result: 01100
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 10010010110011010
    #   Finished 'main' in less than a millisecond

    # # test _checksum
    # for test in [
    #     '1100',
    #     '1001',
    #     '11011000',
    # ]:
    #     print(test, _checksum(test))

    # # test checksum
    # for test in [
    #     '1100',
    #     '1001',
    #     '110110001100',
    #     '110010110100',
    # ]:
    #     print(test, checksum(test))

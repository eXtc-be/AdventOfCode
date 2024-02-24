# aoc_2017_10_A_1.py - Day 10: Knot Hash - part 1
# Once the knot twisting process is complete, what is the result of multiplying the first two numbers in the list?
# https://adventofcode.com/2017/day/10


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_10'

LIST_LENGTH_REAL = 256
LIST_LENGTH_TEST = 5


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_lengths(data: str) -> list[int]:
    return [int(value) for value in data.split(',')]


def _extract_sublist(numbers: list[int], position: int, length: int) -> list[int]:
    if position >= len(numbers):
        raise ValueError(f'Position {position} is out of range')
    if length > len(numbers):
        raise ValueError(f'Length {length} is out of range')

    if position + length > len(numbers):
        return numbers[position:] + numbers[:position+length-len(numbers)]
    else:
        return numbers[position:position+length]


def _insert_sublist(numbers: list[int], sublist: list[int], position: int) -> None:
    if position >= len(numbers):
        raise ValueError(f'Position {position} is out of range')
    if len(sublist) > len(numbers):
        raise ValueError(f'Sublist ({len(sublist)}) is is too long for numbers list ({len(numbers)})')

    for i in range(len(sublist)):
        numbers[(position+i) % len(numbers)] = sublist[i]


def process_lengths(numbers: list[int], lengths: list[int]) -> None:
    position = 0
    skip = 0

    for length in lengths:
        # print(numbers)
        _insert_sublist(
            numbers,
            _extract_sublist(numbers, position, length)[::-1],
            position
        )

        position = (position + length + skip) % len(numbers)
        skip += 1


test_data = '''
3,4,1,5
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], list_length: int = LIST_LENGTH_REAL) -> None:
    lengths = get_lengths(data_lines[0])
    # print(lengths)

    numbers = list(range(list_length))

    process_lengths(numbers, lengths)
    # print(numbers)

    print(f'End result: {numbers[0] * numbers[1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, LIST_LENGTH_REAL)
    # main(data_lines, LIST_LENGTH_TEST)
    # using test_data:
    #   End result: 12
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 20056
    #   Finished 'main' in less than a millisecond

    # # test _get_sublist
    # print(_get_sublist([1, 2, 3, 4, 5], 0, 2))  # [1, 2]
    # print(_get_sublist([1, 2, 3, 4, 5], 0, 5))  # [1, 2, 3, 4, 5]
    # print(_get_sublist([1, 2, 3, 4, 5], 2, 3))  # [3, 4, 5]
    # print(_get_sublist([1, 2, 3, 4, 5], 3, 3))  # [4, 5, 1]
    # print(_get_sublist([1, 2, 3, 4, 5], 3, 4))  # [4, 5, 1, 2]
    # print(_get_sublist([1, 2, 3, 4, 5], 4, 4))  # [5, 1, 2, 3]
    # print(_get_sublist([1, 2, 3, 4, 5], 5, 4))  # ValueError
    # print(_get_sublist([1, 2, 3, 4, 5], 4, 6))  # ValueError

    # # test _insert_sublist
    # for sub, pos in [
    #     ([5, 4, 3, 2, 1], 0),  # [5, 4, 3, 2, 1]
    #     ([5, 4, 3, 2, 1], 1),  # [1, 5, 4, 3, 2]
    #     ([4, 3, 2], 1),  # [1, 4, 3, 2, 5]
    #     ([5, 4, 3], 2),  # [1, 2, 5, 4, 3]
    #     ([1, 5, 4], 3),  # [4, 2, 3, 1, 5]
    #     ([1, 5, 4], 5),  # ValueError
    #     ([1, 2, 3, 4, 5, 6], 2),  # ValueError
    # ]:
    #     numbers = [1, 2, 3, 4, 5]
    #     print(numbers, end=' -> ')
    #     print(sub, pos, end=' -> ')
    #     _insert_sublist(numbers, sub, pos)
    #     print(numbers)  # [1, 4, 3, 2, 5]

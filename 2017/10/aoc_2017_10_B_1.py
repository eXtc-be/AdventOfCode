# aoc_2017_10_B_1.py - Day 10: Knot Hash - part 2
# Treating your puzzle input as a string of ASCII characters, what is the Knot Hash of your puzzle input?
# https://adventofcode.com/2017/day/10


from aoc_2017_10_A_1 import (
    DATA_PATH,
    LIST_LENGTH_REAL,
    load_data,
    # test_data,
    _extract_sublist,
    _insert_sublist,
)

from tools import time_it

# other imports

from pprint import pprint


SUFFIX = [17, 31, 73, 47, 23]

ROUNDS = 64


def get_lengths(data: str) -> list[int]:
    return [ord(char) for char in data] + SUFFIX


def process_lengths(numbers: list[int], lengths: list[int]) -> None:
    position = 0
    skip = 0

    for _ in range(ROUNDS):
        for length in lengths:
            # print(numbers)
            _insert_sublist(
                numbers,
                _extract_sublist(numbers, position, length)[::-1],
                position
            )

            position = (position + length + skip) % len(numbers)
            skip += 1


def hash_numbers(numbers: list[int]) -> list[int]:
    hashed = [0 for _ in range(16)]
    for i in range(16):
        # print(numbers[i*16:(i+1)*16])
        for number in numbers[i*16:(i+1)*16]:
            hashed[i] ^= number

    return hashed


def knothash(data: str, list_length: int = LIST_LENGTH_REAL) -> str:
    lengths = get_lengths(data)
    # print(lengths)

    numbers = list(range(list_length))
    # print(numbers)

    process_lengths(numbers, lengths)
    # print(numbers)

    dense_hash = hash_numbers(numbers)
    # print(dense_hash)

    return ''.join(f"{n:02x}" for n in dense_hash)


test_data = '''
AoC 2017

1,2,3
1,2,4
'''.strip().splitlines()


@time_it
def main(data: str, list_length: int = LIST_LENGTH_REAL) -> None:
    print(f'End result: {knothash(data, list_length)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0], LIST_LENGTH_REAL)
    # for line in data_lines:
    #     main(line, LIST_LENGTH_REAL)
    # using test_data AoC 2017:
    #   End result: 33efeb34ea91902bb2f59c9920caa6cd
    #   Finished 'main' in 5 milliseconds
    # using test_data <empty string>:
    #   End result: a2582a3a0e66e6e86e3812dcb672a272
    #   Finished 'main' in 1 millisecond
    # using test_data 1,2,3:
    #   End result: 3efbe78a8d82f29979031a4aa0b16a9d
    #   Finished 'main' in 3 milliseconds
    # using test_data 1,2,4:
    #   End result: 63960835bcdc130f0b66d7ff4f6a5a8e
    #   Finished 'main' in 3 milliseconds
    # using input data:
    #   End result: d9a7de4a809c56bf3a9465cb84392c8e
    #   Finished 'main' in 18 milliseconds

    # # test hash_numbers
    # numbers = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22] * 16
    # print(hash_numbers(numbers))
    # hex_string = ''.join(f'{n:02x}' for n in hash_numbers(numbers))
    # print(hex_string)

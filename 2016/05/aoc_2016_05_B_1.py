# aoc_2016_05_B_1.py - Day 5: How About a Nice Game of Chess? - part 2
# Given the actual Door ID, what is the password?
# https://adventofcode.com/2016/day/5


from aoc_2016_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    PASSWORD_LENGTH,
    THRESHOLD,
    find_lowest_hash,
)

from tools import time_it

# other imports

from pprint import pprint


PLACEHOLDER = '_'


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    # print(data_lines[0])

    password = [PLACEHOLDER] * PASSWORD_LENGTH
    index = 0
    i = 0

    while any(c == PLACEHOLDER for c in password):
        index, hex_digest = find_lowest_hash(data_lines[0], index+1, THRESHOLD)
        print(f'{i:3} {index:15,} {hex_digest} ', end='')
        if (
                hex_digest[THRESHOLD].isdigit() and
                int(hex_digest[THRESHOLD]) < PASSWORD_LENGTH and
                password[int(hex_digest[THRESHOLD])] == PLACEHOLDER
        ):
            password[int(hex_digest[THRESHOLD])] = hex_digest[THRESHOLD+1]
        print("".join(password))
        i += 1

    print(f'End result: {"".join(password)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 05ace8e3
    #   Finished 'main' in 17 seconds
    # using input data:
    #   End result: 999828ec
    #   Finished 'main' in 30 seconds

# aoc_2017_16_B_1.py - Day 16: Permutation Promenade - part 2
# In what order are the programs standing after their billion dances?
# https://adventofcode.com/2017/day/16


from aoc_2017_16_A_1 import (
    DATA_PATH,
    CHARS,
    CHARS_TEST,
    load_data,
    test_data,
    get_instructions,
    execute_instructions
)

from tools import time_it

# other imports

from pprint import pprint


ROUNDS = 1_000_000_000
ROUNDS_TEST = 2


# other functions


@time_it
def main(data_lines: list[str], programs: tuple[str, ...] = CHARS, rounds: int = ROUNDS) -> None:
    instructions = get_instructions(data_lines[0])
    # print(instructions)

    result = programs
    repeat = None

    for round in range(rounds):
        if round % 1000 == 0:
            print(f'{round:13,} {"".join(result)}')

        result = execute_instructions(result, instructions)
        if result == programs:
            print(f'repeating pattern found after {round+1} rounds')
            repeat = round + 1
            break

    for round in range(rounds % repeat):
        result = execute_instructions(result, instructions)

    print(f'End result: {"".join(result)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    # main(data_lines)
    main(data_lines, CHARS_TEST)
    # main(data_lines, CHARS_TEST, ROUNDS_TEST)
    # using test_data abcde:
    #   End result: abcde
    #   Finished 'main' in less than a millisecond
    # using test_data abcdefghijklmnop:
    #   End result: ghidjklmnopabcef
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: ahgpjdkcbfmneloi
    #   Finished 'main' in 1 second

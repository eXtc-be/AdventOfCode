# aoc_2024_11_A_1.py - Day 11: Plutonian Pebbles - part 1
# How many stones will you have after blinking 25 times?
# https://adventofcode.com/2024/day/11


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2024_11'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


def get_stones(start: str) -> list[int]:
    return [int(el) for el in start.split()]


def transform_stones(stones: list[int]) -> list[int]:
    result = []

    for stone in stones:
        if stone == 0:
            result.append(1)
        elif len(s := str(stone)) % 2 == 0:
            result.append(int(s[:(len(s) // 2)]))
            result.append(int(s[(len(s) // 2):]))
        else:
            result.append(stone * 2024)

    return result


test_data = '''
0 1 10 99 999
125 17
'''.strip().splitlines()


@time_it
def main(data_line: str) -> None:
    stones = get_stones(data_line)
    # print(stones)
    #
    # print(stones := transform_stones(stones))
    # print(stones := transform_stones(stones))
    # print(stones := transform_stones(stones))
    # print(stones := transform_stones(stones))
    # print(stones := transform_stones(stones))
    # print(stones := transform_stones(stones))

    for i in range(25):
        stones = transform_stones(stones)

    print(f'End result: {len(stones)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0])
    # main(test_data[1])

    # using test_data:
    #   End result: 55312
    #   Finished 'main' in 46 milliseconds
    # using input data:
    #   End result: 202019
    #   Finished 'main' in 179 milliseconds

# aoc_2017_05_A_1.py - Day 5: A Maze of Twisty Trampolines, All Alike - part 1
# How many steps does it take to reach the exit?
# https://adventofcode.com/2017/day/5


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_05'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_steps(datalines: list[str]) -> list[int]:
    return [int(line) for line in datalines]


def execute_steps(steps: list[int]) -> int:
    num = 1
    current_step = 0

    while True:
        delta = steps[current_step]
        steps[current_step] += 1
        current_step += delta
        if not 0 <=  current_step < len(steps):
            break
        num += 1

    return num


test_data = '''
0
3
0
1
-3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    steps = get_steps(data_lines)
    # print(steps)

    execute_steps(steps)
    print(steps)

    # print(f'End result: {execute_steps(steps)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 5
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 343467
    #   Finished 'main' in 107 milliseconds

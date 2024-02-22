# aoc_2017_05_B_1.py - Day 5: A Maze of Twisty Trampolines, All Alike - part 2
# How many steps does it take to reach the exit?
# https://adventofcode.com/2017/day/5


from aoc_2017_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_steps,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def execute_steps(steps: list[int]) -> int:
    num = 1
    current_step = 0

    while True:
        delta = steps[current_step]
        if delta >= 3:
            steps[current_step] -= 1
        else:
            steps[current_step] += 1
        current_step += delta
        if not 0 <=  current_step < len(steps):
            break
        num += 1

    return num


@time_it
def main(data_lines: list[str]) -> None:
    steps = get_steps(data_lines)
    # print(steps)

    # num = execute_steps(steps)
    # print(steps, num)

    print(f'End result: {execute_steps(steps)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: [2, 3, 2, 3, -1] 10
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 24774780
    #   Finished 'main' in 6.6 seconds

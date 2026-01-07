# aoc_2025_06_B_1.py - Day 6: Trash Compactor - part 2
# Solve the problems on the math worksheet again. What is the grand total
# found by adding together all the answers to the individual problems?
# https://adventofcode.com/2025/day/6


from aoc_2025_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    process_problem,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions
def get_problems(lines: list[str]) -> list[tuple]:
    numbers = [list(el) for el in zip(*lines)]  # transpose lines

    problems = []
    group = []
    for el in numbers + [' ']:
        if not all(part == ' ' for part in el):
            group.append(el)
            continue
        problem = [int(''.join(member[:-1])) for member in group] + [group[0][-1]]
        problems.append(problem)
        group = []

    return problems


@time_it
def main(data_lines: list[str]) -> None:
    problems = get_problems(data_lines)

    result = sum(process_problem(problem) for problem in problems)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 3263827
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 12377473011151
    #   Finished 'main' in 5 milliseconds

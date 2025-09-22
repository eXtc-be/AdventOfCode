# aoc_2024_02_A_1.py - Day 2: Red-Nosed Reports - part 1
# Analyze the unusual data from the engineers. How many reports are safe?
# https://adventofcode.com/2024/day/2


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2024_02'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


def create_reports(data_lines: list[str]) -> list[list[int]]:
    return [[int(value) for value in line.split()] for line in data_lines]


def create_diffs(reports: list[list[int]]) -> list[list[int]]:
    return [[v1 - v2 for v1, v2 in zip(report, report[1:])] for report in reports]


def check_diff(diff: list[int]) -> bool:
    if any(abs(d) < 1 or abs(d) > 3 for d in diff):
        return False

    first = abs(diff[0]) / diff[0]
    if not all(abs(d) / d == first for d in diff):
        return False

    return True


test_data = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    reports = create_reports(data_lines)
    # print('\n'.join('/'.join(str(value) for value in report) for report in reports))

    diffs = create_diffs(reports)
    # print('\n'.join(':'.join(str(value) for value in diff) for diff in diffs))

    result = sum(1 if check_diff(diff) else 0 for diff in diffs)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 549
    #   Finished 'main' in 4 milliseconds

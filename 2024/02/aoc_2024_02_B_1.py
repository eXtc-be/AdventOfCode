# aoc_2024_02_B_1.py - Day 2: Red-Nosed Reports - part 2
# Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports.
# How many reports are now safe?
# https://adventofcode.com/2024/day/2


from aoc_2024_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_reports,
    create_diffs,
    check_diff
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions

def repair_report(report: list[int]) -> bool:
    for i in range(len(report)):
        candidate = [report[j] for j in range(len(report)) if j != i]
        diff = [v1 - v2 for v1, v2 in zip(candidate, candidate[1:])]
        if check_diff(diff):
            return True

    return False


@time_it
def main(data_lines: list[str]) -> None:
    reports = create_reports(data_lines)
    # print('\n'.join('/'.join(str(value) for value in report) for report in reports))

    diffs = create_diffs(reports)
    # print('\n'.join(':'.join(str(value) for value in diff) for diff in diffs))

    result = sum(1 if check_diff(diff) or repair_report(reports[diffs.index(diff)]) else 0 for diff in diffs)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 589
    #   Finished 'main' in 12 milliseconds

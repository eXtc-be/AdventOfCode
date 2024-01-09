# aoc_2015_05_B_1.py - Day 5: Doesn't He Have Intern-Elves For This? - part 2
# How many strings are nice with the new rules?
# https://adventofcode.com/2015/day/5


from aoc_2015_05_A_1 import (
    DATA_PATH,
    load_data,
)

from tools import time_it

# other imports

from pprint import pprint


P_THRESHOLD = 1
R_THRESHOLD = 1


def check_pairs(string: str, num: int = P_THRESHOLD) -> bool:
    pairs = []
    for i, sub_string in enumerate(zip(string, string[1:-1])):
        if ''.join(sub_string) in string[:i] + '..' + string[i+2:]:
            pairs.append(''.join(sub_string))

    # return pairs
    return len(pairs) >= num


def check_repeats(string: str, num: int = R_THRESHOLD) -> bool:
    repeats = []
    for first, middle, last in zip(string, string[1:], string[2:]):
        if first == last:
            repeats.append(''.join((first, middle, last)))

    # return repeats
    return len(repeats) >= num


def is_nice(string: str) -> bool:
    return (
            check_pairs(string) and
            check_repeats(string)
    )


test_data = '''
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    nice = [line for line in data_lines if is_nice(line)]
    print(nice)

    print(f'End result: {len(nice)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 55
    #   Finished 'main' in 7 milliseconds

    # # test check_pairs
    # for line in 'xyxy aabcdefgaa aaa'.split():
    #     print(line, check_pairs(line))

    # # test check_repeats
    # for line in 'xyx abcdefeghi aaa'.split():
    #     print(line, check_repeats(line))

    # # test both checks with input data
    # for line in data_lines:
    #     print(line, check_pairs(line), check_repeats(line))

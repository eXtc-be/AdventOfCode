# aoc_2023_13_A_1.py - Day 13: Point of Incidence - part 1
# Find the line of reflection in each of the patterns in your notes.
# What number do you get after summarizing all of your notes?
# https://adventofcode.com/2023/day/13


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_13'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_patterns(data_lines: list[str]) -> list[list[list[str]]]:
    patterns = []
    pattern = []

    for line in data_lines:
        if not line:
            if pattern:
                patterns.append(pattern)  # add pattern to patterns
            pattern = []  # start new pattern
        else:
            pattern.append(list(line))

    if pattern:
        patterns.append(pattern)  # add last pattern to patterns

    return patterns


def _is_reflection(pattern: list[list[str]], cursor) -> bool:
    """returns True if pattern can be mirrored around cursor"""

    # decide how much rows need to be compared
    my_range = min(len(pattern) - 2 - cursor, cursor) + 1
    if cursor == 0 or cursor == len(pattern) - 2:
        my_range = 1

    for i in range(my_range):
        if pattern[cursor + i + 1] != pattern[cursor - i]:
            return False

    return True  # if none of the above tests fail the pattern can be mirrored around the cursor


def _get_reflection(pattern: list[list[str]]) -> int:
    """finds the row around which a pattern can be mirrored"""
    for cursor in range(len(pattern) - 1):
        if _is_reflection(pattern, cursor):
            return cursor + 1  # 0-based vs 1-based

    return 0  # if no reflection was found, return 0 so math further down doesn't break


def get_reflection(pattern: list[list[str]]) -> int:
    """finds horizontal and vertical reflection values for pattern (one is usually zero)"""
    horizontal = _get_reflection(pattern)  # find the horizontal value the normal way
    # find the vertical value by finding the horizontal value of the transposed pattern
    vertical = _get_reflection(list(zip(*pattern)))
    return vertical + 100 * horizontal


def summarize(patterns: list[list[list[str]]]):
    reflections = []

    for pattern in patterns:
        reflections.append(get_reflection(pattern))

    return sum(reflections)


test_data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    patterns = get_patterns(data_lines)
    # pprint(patterns)

    summary = summarize(patterns)
    print(summary)

    print(f'End result: {summary}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 405
    #   Finished 'main' in 0 milliseconds
    # using input data:
    #   End result: 34100
    #   Finished 'main' in 2 milliseconds

    # patterns = get_patterns(data_lines)

    # test _is_reflection with pattern known to have horizontal reflection and correct cursor value
    # print(_is_reflection(patterns[1], 3))  # should return True
    # test _is_reflection with pattern known to have horizontal reflection, but wrong cursor value
    # print(_is_reflection(patterns[1], 2))  # should return False
    # test _is_reflection with pattern known to have horizontal reflection, but wrong cursor value - 0
    # print(_is_reflection(patterns[1], 0))  # should return False and not crash
    # test _is_reflection with pattern known to have horizontal reflection, but wrong cursor value - len(pattern)-2
    # print(_is_reflection(patterns[1], 5))  # should return False and not crash
    # test _is_reflection with transposed pattern known to have vertical reflection and correct cursor value
    # print(_is_reflection(list(zip(*patterns[0])), 4))  # should return True
    # test _is_reflection for horizontal reflection with pattern known to have
    #   vertical reflection and partial horizontal reflection
    # print(_is_reflection(patterns[0], 2))  # should return False

    # test _get_reflection with pattern known to have horizontal reflection
    # print(_get_reflection(patterns[1]))  # should return 4

    # test _get_reflection with transposed pattern known to have vertical reflection
    # print(_get_reflection(list(zip(*patterns[0]))))  # should return 5

    # test get_reflection with pattern known to have horizontal reflection
    # print(get_reflection(patterns[1]))  # should return 400

    # test _get_reflection with transposed pattern known to have vertical reflection
    # print(_get_reflection(list(zip(*patterns[0]))))  # should return 5


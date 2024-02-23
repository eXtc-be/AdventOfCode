# aoc_2017_09_A_1.py - Day 9: Stream Processing - part 1
# What is the total score for all groups in your input?
# https://adventofcode.com/2017/day/9


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_09'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _find_garbage(string: str) -> tuple[int, int]:
    start = stop = -1
    cancel_next = False

    for i, char in enumerate(string):
        if start < 0:
            if char == '<':
                start = i
        else:
            if cancel_next:
                cancel_next = False
                continue
            match char:
                case '>':
                    stop = i+1
                    break
                case '!':
                    cancel_next = True

    return start, stop


def _remove_all_garbage(string: str) -> str:
    while True:
        start, stop = _find_garbage(string)
        if start < 0 or stop < 0:  # no more garbage found
            return string
        string = string[:start] + string[stop:]


def calc_score(string: str) -> int:
    total = 0
    level = 0

    for char in _remove_all_garbage(string):
        if char == '{':
            level += 1
            total += level
        elif char == '}':
            level -= 1

    return total


test_data = '''
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{{},{{},{{}}}}
{<{},{},{{}}>}
{<a>,<a>,<a>,<a>}
{{<a>},{<a>},{<a>},{<a>}}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<!>},{<!>},{<!>},{<a>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}
'''.strip().splitlines()

test_garbage = '''
<>
<random characters>
<<<<>
<{!>}>
<!!>
<!!!>>
<{o"i!a,<{i<a>
{{<a>},{<a>},{<a>},{<a>}}
{{<!>},{<!>},{<!>},{<a>}}
'''.strip().splitlines()

test_groups = '''
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{<{},{},{{}}>}
{<a>,<a>,<a>,<a>}
{{<a>},{<a>},{<a>},{<a>}}
{{<!>},{<!>},{<!>},{<a>}}
{{},{{},{{}}}}
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # # test _find_garbage
    # for line in test_garbage:
    #     start, stop = _find_garbage(line)
    #     if start < 0 or stop < 0:
    #         print(line, start, stop, 'could not find any garbage')
    #     else:
    #         print(line, start, stop, line[start:stop])

    # # test _remove_all_garbage
    # for line in test_groups:
    #     print(line, _remove_all_garbage(line))

    # print(_remove_all_garbage(data_lines[0]))

    # # test calc_score
    # for line in data_lines:
    #     score = calc_score(line)
    #     print(line, score)

    score = calc_score(data_lines[0])

    print(f'End result: {score}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 1, 6, 5, 16, 15, 1, 1, 9, 9, 9, 3, 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 20530
    #   Finished 'main' in 241 milliseconds

# aoc_2018_08_A_1.py - Day 8: Memory Maneuver - part 1
# What is the sum of all metadata entries?
# https://adventofcode.com/2018/day/8
# found on https://old.reddit.com/r/adventofcode/comments/a47ubw/2018_day_8_solutions/ebc7ol0/

from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_08'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_definitions(data: str) -> list[int]:
    return [int(part) for part in data.split()]


def parse(data):
    children, metas = data[:2]
    data = data[2:]
    scores = []
    totals = 0

    for i in range(children):
        total, score, data = parse(data)
        totals += total
        scores.append(score)

    totals += sum(data[:metas])

    if children == 0:
        return (
            totals,
            sum(data[:metas]),
            data[metas:]
        )
    else:
        return (
            totals,
            sum(scores[k - 1] for k in data[:metas] if 0 < k <= len(scores)),
            data[metas:]
        )


test_data = '''
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    data = get_definitions(data_lines[0])
    # print(definitions)

    total, value, remaining = parse(data)
    # print(total, value, remaining)

    print(f'End result: {total}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 138
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 42501
    #   Finished 'main' in 119 milliseconds

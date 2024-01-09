# aoc_2015_02_A_1.py - Day 2: I Was Told There Would Be No Math - part 1
# How many total square feet of wrapping paper should they order?
# https://adventofcode.com/2015/day/2


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_02'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def calc_paper(dimensions: str) -> int:
    l, w, h = (int(d) for d in dimensions.split('x'))
    a1, a2, a3 = l * w, w * h, h * l
    return 2 * a1 + 2 * a2 + 2 * a3 + min(a1, a2, a3)


def calc_total_paper(data_lines: list[str]) -> int:
    return sum(calc_paper(line) for line in data_lines)


test_data = '''
2x3x4
1x1x10
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    paper = calc_total_paper(data_lines)

    print(f'End result: {paper}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 1586300
    #   Finished 'main' in 2 milliseconds

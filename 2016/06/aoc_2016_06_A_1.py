# aoc_2016_06_A_1.py - Day 6: Signals and Noise - part 1
# Given the recording in your puzzle input, what is the error-corrected version of the message being sent?
# https://adventofcode.com/2016/day/6


from tools import time_it

from collections import Counter

from pprint import pprint


DATA_PATH = './input_2016_06'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    message = ''

    for i in range(len(data_lines[0])):
        counter = Counter()
        for line in data_lines:
            counter[line[i]] += 1
        message += counter.most_common()[0][0]

    print(f'End result: {message}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: easter
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: kjxfwkdh
    #   Finished 'main' in 1 millisecond

# aoc_2016_15_A_1.py - Day 15: Timing is Everything - part 1
# What is the first time you can press the button to get a capsule?
# https://adventofcode.com/2016/day/15
# Naive but simple strategy: increment T until a capsule is released with the given layout
#   (it appears this strategy isn't as naive as I first thought: part 1 was solved in 94 ms, part 2 in 2.6 s)


from tools import time_it

from dataclasses import dataclass

from pprint import pprint


DATA_PATH = './input_2016_15'

# other constants


@dataclass
class Disc:
    positions: int
    start_position: int

    def current_position(self, t: int):
        return (self.start_position + t) % self.positions


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_discs(datalines: list[str]) -> dict[int, Disc]:
    return {int(line.split()[1][1:]): Disc(int(line.split()[3]), int(line.split()[-1][:-1])) for line in datalines}


def find_solution(discs: dict[int, Disc]) -> int:
    tp = 0
    while True:
        if all(discs[dt].current_position(tp+dt) == 0 for dt in discs):  # the number of the disc is equal to its offset
            return tp
        tp += 1


test_data = '''
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    discs = get_discs(data_lines)
    # pprint(discs)

    solution = find_solution(discs)

    print(f'End result: {solution}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 5
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 121834
    #   Finished 'main' in 94 milliseconds

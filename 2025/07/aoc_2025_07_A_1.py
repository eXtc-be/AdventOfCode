# aoc_2025_07_A_1.py - Day 7: Laboratories - part 1
# Analyze your manifold diagram. How many times will the beam be split?
# https://adventofcode.com/2025/day/7


from tools import time_it

# other imports

from pprint import pprint
import re


DATA_PATH = './input_2025_07'

# other constants


# classes


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def split_beam(lines: list[str]) -> int:
    total_splits = 0
    beam_positions = set()

    # find the starting point
    beam_positions.add(lines[0].index('S'))

    for line in lines[1:]:
        new_positions = []
        old_positions = []
        for splitter in [m.start() for m in re.finditer(r'\^', line)]:
            if splitter in beam_positions:
                total_splits += 1
                new_positions += [splitter-1, splitter+1]
                old_positions += [splitter]
            else:
                pass

        beam_positions = {beam_position for beam_position in beam_positions if beam_position not in old_positions}
        beam_positions.update(new_positions)

    return total_splits


test_data = '''
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    splits = split_beam(data_lines)
    # splits, timelines = split_beam(data_lines)

    print(f'End result: {splits}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 21
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1698
    #   Finished 'main' in 3 milliseconds

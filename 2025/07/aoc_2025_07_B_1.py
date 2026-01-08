# aoc_2025_07_B_1.py - Day 7: Laboratories - part 2
# Apply the many-worlds interpretation of quantum tachyon splitting to your
# manifold diagram. In total, how many different timelines would a single
# tachyon particle end up on?
# https://adventofcode.com/2025/day/7

# attempt 1: counting the number of beam positions on each line containing splitters and adding them up
# doesn't work, answer is too low


from aoc_2025_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint
import re


# other constants


# other functions
def split_beam(lines: list[str]) -> int:
    total_splits = 0
    total_timelines = 0
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

        total_timelines += len(beam_positions) if '^' in line else 0

    return total_timelines


@time_it
def main(data_lines: list[str]) -> None:
    timelines = split_beam(data_lines)

    print(f'End result: {timelines}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 40
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 3060 -- too low
    #   Finished 'main' in 2 milliseconds

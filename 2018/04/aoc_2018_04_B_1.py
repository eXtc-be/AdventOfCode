# aoc_2018_04_B_1.py - Day 4: Repose Record - part 2
# What is the ID of the guard you chose multiplied by the minute you chose?
# https://adventofcode.com/2018/day/4
from collections import defaultdict

from aoc_2018_04_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_events,
    get_overlap,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    guards = get_events(data_lines)
    # pprint(guards)

    guard_totals = {}
    for guard in guards:
        guard_totals[guard] = get_overlap(guards, guard)
    # pprint(guard_totals)

    winner = max(guard_totals.items(), key=lambda g: g[1][1])
    # print(winner)

    print(f'End result: {winner[0] * winner[1][0]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 4455
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 58559
    #   Finished 'main' in 3 milliseconds

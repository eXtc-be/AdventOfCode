# aoc_2023_14_B_2.py - Day 14: Parabolic Reflector Dish - part 2
# Tilt the platform a large number of times.
# Afterward, what is the total load on the north support beams?
# first optimization: compare the current total load with the previous one and if the value stays stable
#   long enough, i.e. after CUTOFF cycles with the same value, quit early instead of doing all cycles
# turns out this isn't a good optimizing strategy: the value of load is changing so much the number of
#   cycles with an equal value never gets past 2
# https://adventofcode.com/2023/day/14


from aoc_2023_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_grid,
    tilt_grid,
    calc_load,
)

from aoc_2023_14_B_1 import (
    cycle_grid,
)

from tools import time_it

# other imports

from pprint import pprint


# CYCLES = 1_000
CYCLES = 100_000
# CYCLES = 1_000_000
# CYCLES = 1_000_000_000

CUTOFF = 10
# CUTOFF = 1_000


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)

    equal = 0
    previous = -1
    cycled_grid = grid
    for cycle in range(CYCLES):
        cycled_grid = cycle_grid(cycled_grid)
        total_load = sum(calc_load(cycled_grid))
        if total_load == previous:
            equal += 1
            if equal >= CUTOFF:
                break
        else:
            previous = total_load
            print(equal)
            equal = 0

    loads = calc_load(cycled_grid)
    print(loads)

    print(f'End result: {sum(loads)} after {cycle+1:,} cycles')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 64 after 1,000 cycles
    #   Finished 'main' in 154 milliseconds
    #   End result: 64 after 1,000 cycles (optimized)
    #   Finished 'main' in 152 milliseconds
    #   End result: 65 after 100,000 cycles (optimized)
    #   Finished 'main' in 14 seconds
    #   End result: 63 after 1,000,000 cycles
    #   Finished 'main' in 2 minutes and 29 seconds
    #   End result: 63 after 1,000,000 cycles (optimized)
    #   Finished 'main' in 2 minutes and 30 seconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

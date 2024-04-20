# aoc_2023_14_B_4.py - Day 14: Parabolic Reflector Dish - part 2
# Tilt the platform a large number of times.
# Afterward, what is the total load on the north support beams?
# third optimization: read somewhere on the interwebs that the value of load has a cycle,
#   so this time we're going to determine the cycle length and extrapolate to find the result
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

from find_cycles import (
    find_cycle,
)

from tools import time_it

# other imports

from pprint import pprint


CYCLES = 1_000
# CYCLES = 100_000
# CYCLES = 1_000_000
# CYCLES = 1_000_000_000

@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)

    cycled_grid = grid
    output = []
    for _ in range(1000):
        cycled_grid = cycle_grid(cycled_grid)
        output.append(sum(calc_load(cycled_grid)))

    # print(output)

    offset, cycle = find_cycle(output)
    # print(offset, cycle)

    next_value_idx = (CYCLES - offset - 1) % len(cycle)
    # print(next_value_idx)

    predicted_load = cycle[next_value_idx]

    print(f'End result: {predicted_load} - cycle length: {len(cycle)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 64 - cycle length: 7
    #   Finished 'main' in 459 milliseconds
    # using input data:
    #   End result: 88371 - cycle length: 72
    #   Finished 'main' in 13 seconds

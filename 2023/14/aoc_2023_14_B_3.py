# aoc_2023_14_B_3.py - Day 14: Parabolic Reflector Dish - part 2
# Tilt the platform a large number of times.
# Afterward, what is the total load on the north support beams?
# second optimization: keep a running average of the values for load and
#   cutoff after CUTOFF cycles with the same average
# this strategy works better than the previous one, but not good enough
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

# CUTOFF = 10
# CUTOFF = 100
CUTOFF = 1_000
# CUTOFF = 10_000


@time_it
def main(data_lines: list[str]) -> None:
    grid = create_grid(data_lines)

    equal = 0
    running_total = 0
    previous = -1
    cycled_grid = grid
    for cycle in range(CYCLES):
        cycled_grid = cycle_grid(cycled_grid)
        running_total += sum(calc_load(cycled_grid))
        if running_total // (cycle + 1) == previous:
            equal += 1
            if equal >= CUTOFF:
                break
        else:
            previous = running_total // (cycle + 1)
            # print(equal)
            equal = 0

    load = running_total // (cycle + 1)

    print(f'End result: {load} after {cycle+1:,}/{CYCLES:,} cycles, cutoff at {CUTOFF:,}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 67 after 24/1,000 cycles, cutoff at 10
    #   Finished 'main' in 4 milliseconds
    #   End result: 66 after 134 cycles/100_000, cutoff at 100
    #   Finished 'main' in 21 milliseconds
    #   End result: 66 after 1,034/1_000_000 cycles, cutoff at 1_000
    #   Finished 'main' in 156 milliseconds
    #   End result: 66 after 10,034/1,000,000,000 cycles, cutoff at 10,000
    #   Finished 'main' in 1.57 seconds
    # using input data:
    #   End result: 88609 after 1,000/1,000 cycles, cutoff at 10 (too high)
    #   Finished 'main' in 13 seconds
    #   End result: 88599 after 1,049/100,000 cycles, cutoff at 10 (not submitted)
    #   Finished 'main' in 13 seconds
    #   End result: 88390 after 5,375/100,000 cycles, cutoff at 100 (not submitted)
    #   Finished 'main' in 1 minute and 8 seconds
    #   End result: 88354 after 18,619/100,000 cycles, cutoff at 1,000
    #   Finished 'main' in 3 minutes and 59 seconds
    #   End result: xxx
    #   Finished 'main' in xxx

    # test _rotate_grid
    # n_grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    # draw_grid(n_grid)
    #
    # e_grid = _rotate_grid(n_grid,'E')
    # draw_grid(e_grid)
    #
    # s_grid = _rotate_grid(n_grid,'S')
    # draw_grid(s_grid)
    #
    # w_grid = _rotate_grid(n_grid,'W')
    # draw_grid(w_grid)

    # test cycle_grid
    # cycled_grid = cycle_grid(grid)
    # draw_grid(cycled_grid)
    # cycled_grid = cycle_grid(cycled_grid)
    # draw_grid(cycled_grid)
    # cycled_grid = cycle_grid(cycled_grid)
    # draw_grid(cycled_grid)


# aoc_2019_14_B_extern_1a.py - Day 14: Space Stoichiometry - part 2
# Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?
# https://adventofcode.com/2019/day/14
# based on the solution from Alexandre Martins: https://asmartins.com/blog/rocket-fuel/
# using the bisect method


from aoc_2019_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from aoc_2019_14_A_extern_1a import (
    get_reactions
)

from aoc_2019_14_A_extern_1b import (
    order_chemicals,
    ore_required,
)

from tools import time_it

from typing import Callable
import math

from pprint import pprint


NUMBER = int(1E12)


def bisect(function: Callable, target: int, interval: tuple[int, int], args: tuple = ()) -> tuple[int, int]:
    iterations = 0

    low, high = interval
    while low <= high:
        iterations += 1

        mid = low + (high-low)//2
        f_mid = function((mid, 'FUEL'), *args)

        if f_mid == target:
            return mid, iterations
        if f_mid < target:
            low = mid + 1
        else:
            high = mid - 1

    return low-1, iterations


def get_bounds(reactions: dict[str, tuple[int, list[tuple[int, str]]]], ordering: dict[str, int], available: int):
    ratio, _ = ore_required(reactions, ordering, (1, 'FUEL'))

    under_estimation = available // ratio
    order = int(math.log10(under_estimation))
    wanted = 10**order
    needed, _ = ore_required(reactions, ordering, (wanted, 'FUEL'))

    while needed < available:
        print(wanted)
        order += 1
        wanted = 10**order
        needed, _ = ore_required(reactions, ordering, (wanted, 'FUEL'))

    ratio = math.floor(available / wanted)
    over_estimation = available // ratio
    return (under_estimation, over_estimation), order


@time_it
def main(data_lines: list[str]) -> None:
    reactions = get_reactions(data_lines)
    # pprint(reactions)

    def f(goal, reactions, ordering):
        ore, _ = ore_required(reactions, ordering, goal)
        return ore

    ordering = order_chemicals(reactions, 'FUEL')
    args = (reactions, ordering)
    estimations, _ = get_bounds(reactions, ordering, NUMBER)
    result, iterations = bisect(f, NUMBER, estimations, args)

    print(f'End result: {result} ({iterations} iterations)')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    main(test_data[2])
    main(test_data[3])
    main(test_data[4])

    # using test_data 2:
    #   End result: 82892753 (30 iterations)
    #   Finished 'main' in 1 millisecond
    # using test_data 3:
    #   End result: 5586022 (25 iterations)
    #   Finished 'main' in 1 millisecond
    # using test_data 4:
    #   End result: 460664 (22 iterations)
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 2876992 (24 iterations)
    #   Finished 'main' in 5 milliseconds

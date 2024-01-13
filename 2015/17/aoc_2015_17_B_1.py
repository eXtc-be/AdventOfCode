# aoc_2015_17_B_1.py - Day 17: No Such Thing as Too Much - part 2
# Find the minimum number of containers that can exactly fit all 150 liters of eggnog.
# How many different ways can you fill that number of containers and still hold exactly 150 litres?
# https://adventofcode.com/2015/day/17


from aoc_2015_17_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_containers,
    get_combos,
    TOTAL
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    containers = get_containers(data_lines)
    # print(containers)

    combos = get_combos(containers)
    # pprint(list(combos))

    good_combos = [combo for combo in combos if sum(combo) == TOTAL]
    # pprint(good_combos)

    minimal_containers = min(len(combo) for combo in good_combos)
    good_combos = [combo for combo in good_combos if len(combo) == minimal_containers]
    # pprint(good_combos)

    print(f'End result: {len(good_combos)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 18
    #   Finished 'main' in 313 milliseconds

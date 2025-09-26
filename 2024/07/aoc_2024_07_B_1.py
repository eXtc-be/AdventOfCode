# aoc_2024_07_B_1.py - Day 7: Bridge Repair - part 2
# Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
# https://adventofcode.com/2024/day/7


from aoc_2024_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    OPERATORS,
    Equation,
    create_equations,
    solve_equation,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants

OPERATORS['||'] = lambda n1, n2: int(str(n1) + str(n2))


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    equations = create_equations(data_lines)
    result = sum(eq.result if solve_equation(eq) else 0 for eq in equations)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 11387
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 456565678667482
    #   Finished 'main' in 21 seconds

# aoc_2018_18_B_1.py - Day 18: Settlers of The North Pole - part 2
# What will the total resource value of the lumber collection area be after 1.000.000.000 minutes?
# https://adventofcode.com/2018/day/18


import sys
sys.path.extend(['.', '..', '../..'])


from aoc_2018_18_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_grid,
    do_step,
    score_grid,
    print_grid,
    clear,
)

from tools import time_it

# other imports

from pprint import pprint


STEPS = 1_000_000_000


def find_repeating_sequence(numbers: list[int]) -> tuple[int | None, int | None]:
    """returns the start index and length if any repeating sequence was found, None otherwise"""
    for length in range(2, len(numbers) // 2 + 1):
        for offset in range(len(numbers) - 2 * length):
            if numbers[offset:offset+length] == numbers[offset+length:offset+length+length]:
                return offset, length

    return None, None


@time_it
def main(data_lines: list[str], verbose: bool = False) -> None:
    grid = get_grid(data_lines)
    # pprint(grid)

    scores = []
    step, start, length = None, None, None

    for step in range(STEPS):
        if verbose:
            clear()
            print(f'Step: {step} - Score: {score_grid(grid)}')
            print_grid(grid)
            # input('Press Enter to continue...')
        else:
            print(f'Step: {step} - Score: {score_grid(grid)}')

        # check for repeating sequences
        scores.append(score_grid(grid))
        start, length = find_repeating_sequence(scores)
        if start and length:
            break

        grid = do_step(grid)

    print(f'Repeating sequence found at step {step}')

    todo = (STEPS - start) % length

    print(f'Doing another ({STEPS} - {start}) % {length} = {todo} steps.')

    for step in range(step+1, step+1+todo):
        if verbose:
            clear()
            print(f'Step: {step} - Score: {score_grid(grid)}')
            print_grid(grid)
            # input('Press Enter to continue...')
        else:
            print(f'Step: {step} - Score: {score_grid(grid)}')
        grid = do_step(grid)

    print(f'\nEnd result: {score_grid(grid)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH), True)
    # main(test_data, True)

    # using input data:
    #   End result: 196310
    #   Finished 'main' in 12 seconds

    # # test find_repeating_sequence
    # for test in [
    #     [3, 0, 5, 5, 1, 5, 1, 6, 8],
    #     [2, 0, 6, 3, 1, 6, 3, 1, 6, 3, 1],
    # ]:
    #     start, stop = find_repeating_sequence(test)
    #     print(test, start, stop, test[start:start+stop])

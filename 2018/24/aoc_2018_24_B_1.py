# aoc_2018_24_B_1.py - Day 24: Immune System Simulator 20XX - part 2
# How many units does the immune system have left after getting the smallest boost it needs to win?
# https://adventofcode.com/2018/day/24


from aoc_2018_24_A_1 import (
    DATA_PATH,
    Battle,
    load_data,
    get_units,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str], boost_start: int = 1, verbose: bool = False, confirm: bool = False) -> None:
    boost = boost_start
    units_left = 0

    while True:
        print(f'Trying boost {boost}:')
        if verbose:
            print('=' * 100)

        immune, infection = get_units(data_lines, boost)

        battle = Battle([immune, infection])
        loser, units_left = battle.do_battle(verbose=verbose, confirm=confirm)

        if loser == 'immune' or loser == '':
            if loser == '':
                print(f'\tStalemate with total {units_left} units left.')
            else:
                print(f'\tInfection won with {units_left} units left.')
            boost += 1
            # break
        else:
            break

    print(f'\tImmune won with {units_left} units left.\n')
    print(f'End result: {units_left}')


if __name__ == "__main__":
    main(load_data(DATA_PATH), boost_start=50, verbose=False)
    # main(test_data, boost_start=1, verbose=False, confirm=False)

    # using test_data:
    #   End result: 51
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 10954 - boost 51
    #   Finished 'main' in 6.0 seconds

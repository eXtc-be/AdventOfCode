# aoc_2018_09_B_1.py - Day 9: Marble Mania - part 2
# What would the new winning Elf's score be if the number of the last marble were 100 times larger?
# https://adventofcode.com/2018/day/9
# this (naive) strategy just uses the solution from part 1, but because inserting and deleling elements
# in an array becomes slower the more elements there are, this is running way too slow


from aoc_2018_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_rules,
    draw_marbles,
    do_turn,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data: str, verbose: bool = False) -> None:
    global turn_len, player_len

    players, turns = get_rules(data)
    turns *= 100

    turn_len = len(f'{turns}')
    player_len = len(f'{players}')

    scores = [0] * players

    marbles = [0]
    current = 0
    if verbose:
        draw_marbles(marbles, current, 0, 0)

    for turn in range(turns):
        current, score = do_turn(marbles, current, turn + 1)
        scores[turn % players] += score
        if verbose:
            draw_marbles(marbles, current, turn + 1, turn % players + 1)
        elif turn % 1000 == 0:
            print(f'{turn}')

    if verbose:
        print(scores)
        print(marbles)

    print(f'End result: {max(scores)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])

    # using input data:
    #   End result: ???
    #   Finished 'main' in ???

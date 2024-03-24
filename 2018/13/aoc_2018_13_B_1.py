# aoc_2018_13_B_1.py - Day 13: Mine Cart Madness - part 2
# What is the location of the last cart at the end of the first tick where it is the only cart left?
# https://adventofcode.com/2018/day/13


from aoc_2018_13_A_2 import (
    DATA_PATH,
    load_data,
    # test_data,
    clear,
    read_input,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


# test_data = r'''
# />-<\
# |   |
# | /<+-\
# | | | |
# \-+-/ |
#   |   |
#   \<->/
# '''.strip().splitlines()

test_data = r'''
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], step: bool = False, verbose: bool = False) -> None:
    track = read_input(data_lines)
    # pprint(track)
    if verbose:
        print(track)
        # print('-' * 100)
    else:
        print(track.tick)

    while True:
        if step:
            input('Press Enter to continue')

        track.do_tick()
        if verbose:
            clear()
            print(track)
            # print('-' * 100)
        else:
            if track.tick % 100 == 0:
                print(track.tick)

        if any(cart.crashed for cart in track.carts):
            track.remove_collided()
            if len(track.carts) == 1:
                break

    print(f'End result: {track.carts[0].location.x},{track.carts[0].location.y} in {track.tick} ticks')


if __name__ == "__main__":
    main(load_data(DATA_PATH), step=False, verbose=False)
    # main(test_data)
    # main(test_data, step=False, verbose=True)

    # using test_data:
    #   End result: 6,4 in 3 ticks
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 53,111 in 12619 ticks
    #   Finished 'main' in 1 second

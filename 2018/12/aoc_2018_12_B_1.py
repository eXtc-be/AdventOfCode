# aoc_2018_12_B_1.py - Day 12: Subterranean Sustainability - part 2
# After 50,000,000,000 generations, what is the sum of the numbers of all pots which contain a plant?
# https://adventofcode.com/2018/day/12

# running the program longer reveals a pattern: from step 185 onwards (worth 35211) every step adds 194 to the total,
# so to calculate the nth generation: S = (n - 185) * 194 + 35,211
# so, if n = 200, S = (200 - 185) * 194 + 35,211 = 38,121
#     if n = 500, S = (200 - 185) * 194 + 35,211 = 96.321


from aoc_2018_12_A_1 import (
    DATA_PATH,
    BOLD, ENDC,
    PLANT, EMPTY,
    load_data,
    test_data,
    get_data,
    do_turn
)

from tools import time_it

# other imports

from pprint import pprint


TURNS = 50_000_000_000


# other functions


@time_it
def main(data_lines: list[str], turns: int = TURNS, verbose: bool = False) -> None:
    initial_state, rules = get_data(data_lines)
    # print(initial_state)
    # pprint(rules)

    turn_len = len(f'{turns:,}')

    state = initial_state
    start = 0
    previous = 0
    total = sum(i + start for i, c in enumerate(state) if c == PLANT)
    if verbose:
        print(
            f'{0:{turn_len},}: '
            f'[{total:{turn_len*2},}] [{(total - previous):{turn_len*2},}]'
            f'{state}'
        )
    previous = total
    for turn in range(turns):
        state, start = do_turn(state, start, rules)
        total = sum(i + start for i, c in enumerate(state) if c == PLANT)
        if verbose:
            print(
                f'{turn+1:{turn_len},}: '
                f'[{total:{turn_len*2},}] [{(total-previous):{turn_len*2},}]'
                f'{"".join(BOLD+c+ENDC if i+start==0 else c for i, c in enumerate(state))} '
            )
        else:
            if (turn+1) % 1000 == 0 or turns < 500:
                print(
                    f'{turn+1:{turn_len},}: '
                    f'[{total:{turn_len*2},}] [{(total-previous):{turn_len*2},}]'
                )
        previous = total

    print(f'End result: {sum(i+start for i, c in enumerate(state) if c==PLANT)}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH), 500, True)
    # main(test_data)

    print(f'End result: {(TURNS - 185) * 194 + 35211}')

    # using input data:
    #   End result: 9699999999321

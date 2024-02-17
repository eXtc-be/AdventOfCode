# aoc_2016_20_B_1.py - Day 20: Firewall Rules - part 2
# How many IPs are allowed by the blacklist?
# https://adventofcode.com/2016/day/20


from aoc_2016_20_A_2 import (
    DATA_PATH,
    load_data,
    test_data,
    LO,
    HI,
    Entry,
    get_blacklist,
    calc_whitelist,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str], lo: int = LO, hi: int = HI) -> None:
    blacklist = get_blacklist(data_lines)
    # print(blacklist)

    whitelist = calc_whitelist(Entry(lo, hi), blacklist)
    # print(whitelist)

    print(f'End result: {sum(white.hi+1 - white.lo for white in whitelist)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, LO, HI)
    # main(data_lines, 0, 9)
    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 104
    #   Finished 'main' in 22 milliseconds

# aoc_2016_20_A_1.py - Day 20: Firewall Rules - part 1
# What is the lowest-valued IP that is not blocked?
# https://adventofcode.com/2016/day/20
# strategy 2: determine how the set would look by calculating overlaps instead of brute forcing it


from tools import time_it

from typing import NamedTuple

from pprint import pprint


DATA_PATH = './input_2016_20'

LO, HI = 0, 4294967295


class Entry(NamedTuple):
    lo: int
    hi: int


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_blacklist(datalines: list[str]) -> list[Entry]:
    return [Entry(int(line.split('-')[0]), int(line.split('-')[1])) for line in datalines]


def _find_overlaps(whitelist: list[Entry], entry: Entry) -> list[Entry]:
    return [
        Entry(max(w.lo, entry.lo), min(w.hi, entry.hi))
        for w in whitelist
        if w.lo <= entry.lo <= w.hi or w.lo <= entry.hi <= w.hi
    ]


def calc_whitelist(start_entry: Entry, blacklist: list[Entry]) -> list[Entry]:
    whitelist = [start_entry]
    lo, hi = start_entry.lo, start_entry.hi
    for entry in sorted(blacklist):
        # print(entry)
        new_list = []
        while whitelist:
            white = whitelist.pop(0)
            if white.lo <= entry.lo <= white.hi:
                # entry's lo value is between white's lo and hi values
                if white.lo <= entry.hi <= white.hi:
                    # AND entry's hi value is between white's lo and hi values
                    # -> split white into (white.lo, entry.lo-1) and (entry.hi+1, white.hi)
                    new_list.append(Entry(white.lo, entry.lo-1))
                    new_list.append(Entry(entry.hi + 1, white.hi))
                else:
                    # AND entry's hi value is NOT between white's lo and hi values
                    # -> replace white with (white.lo, entry.lo-1)
                    new_list.append(Entry(white.lo, entry.lo-1))
            elif white.lo <= entry.hi <= white.hi:
                # entry's lo value is NOT between white's lo and hi values
                # AND entry's hi value is between white's lo and hi values
                # -> replace white with (entry.hi+1, white.hi)
                new_list.append(Entry(entry.hi+1, white.hi))
            else:
                # no overlap whatsoever between white and entry
                # -> re-add white
                new_list.append(white)
        whitelist = new_list
        # print(whitelist)

    return [white for white in whitelist if white.hi >= white.lo]


# test_data = '''
# 0-2
# 3-7
# 5-8
# '''.strip().splitlines()

# test_data = '''
# 0-2
# 4-7
# 5-9
# '''.strip().splitlines()

test_data = '''
5-8
0-2
4-7
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], lo: int = LO, hi: int = HI) -> None:
    blacklist = get_blacklist(data_lines)
    # print(blacklist)

    whitelist = calc_whitelist(Entry(lo, hi), blacklist)
    # print(whitelist)

    print(f'End result: {[white.lo for white in sorted(whitelist)][0]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, LO, HI)
    # main(data_lines, 0, 9)
    # using test_data:
    #   End result: 3, 3, 9
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 17348574
    #   Finished 'main' in 22 milliseconds

    # # test _find_overlaps
    # whitelist = [Entry(3, 5), Entry(8, 11)]
    # print(_find_overlaps(whitelist, Entry(4, 9)))  # [Entry(lo=4, hi=5), Entry(lo=8, hi=9)]
    # print(_find_overlaps(whitelist, Entry(1, 4)))  # [Entry(lo=3, hi=4)]
    # print(_find_overlaps(whitelist, Entry(10, 13)))  # [Entry(lo=10, hi=11)]
    # print(_find_overlaps(whitelist, Entry(1, 2)))  # []
    # print(_find_overlaps(whitelist, Entry(6, 7)))  # []
    # print(_find_overlaps(whitelist, Entry(12, 13)))  # []

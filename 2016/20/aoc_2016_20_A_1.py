# aoc_2016_20_A_1.py - Day 20: Firewall Rules - part 1
# What is the lowest-valued IP that is not blocked?
# https://adventofcode.com/2016/day/20
# strategy 1: make a set with all the numbers between LO and HI,
#   loop over the blacklist and exclude any entries that match the blacklist
#   by using set.difference() (s1 - s2)
#   for the input data (0-4294967295) this took several minutes to try to create the set,
#   and then the program crashed with a MemoryError


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


def get_whitelist(start_entry: Entry, blacklist: list[Entry]) -> set[int]:
    whitelist = {n for n in range(start_entry.lo, start_entry.hi + 1)}
    for entry in sorted(blacklist):
        print(entry)
        whitelist = whitelist.difference({n for n in range(entry.lo, entry.hi + 1)})

    return whitelist


test_data = '''
5-8
0-2
4-7
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], lo: int = LO, hi: int = HI) -> None:
    blacklist = get_blacklist(data_lines)
    # print(blacklist)

    whitelist = get_whitelist(Entry(lo, hi), blacklist)
    # print(whitelist)

    print(f'End result: {min(whitelist)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, LO, HI)
    # main(data_lines, 0, 10)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: MemoryError
    #   Finished 'main' in several minutes

    # # test _find_overlaps
    # whitelist = [Entry(3, 5), Entry(8, 11)]
    # print(_find_overlaps(whitelist, Entry(4, 9)))  # [Entry(lo=4, hi=5), Entry(lo=8, hi=9)]
    # print(_find_overlaps(whitelist, Entry(1, 4)))  # [Entry(lo=3, hi=4)]
    # print(_find_overlaps(whitelist, Entry(10, 13)))  # [Entry(lo=10, hi=11)]
    # print(_find_overlaps(whitelist, Entry(1, 2)))  # []
    # print(_find_overlaps(whitelist, Entry(6, 7)))  # []
    # print(_find_overlaps(whitelist, Entry(12, 13)))  # []

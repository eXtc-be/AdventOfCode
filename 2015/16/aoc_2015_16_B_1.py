# aoc_2015_16_B_1.py - Day 16: Aunt Sue - part 2
# What is the number of the Sue that got you the gift?
# https://adventofcode.com/2015/day/16


from aoc_2015_16_A_1 import (
    DATA_PATH,
    load_data,
    MFCSAM,
    get_mfcsam,
    get_aunts,
)

from tools import time_it

from operator import eq, gt, lt

from pprint import pprint


PROPERTY_MAP = {
    'children': eq,
    'cats': gt,
    'samoyeds': eq,
    'pomeranians': lt,
    'akitas': eq,
    'vizslas': eq,
    'goldfish': lt,
    'trees': gt,
    'cars': eq,
    'perfumes': eq,
}


def filter_aunts(aunt: dict[str, int], mfcsam: dict[str, int]) -> bool:
    for property, value in mfcsam.items():
        if property in aunt:
            if not PROPERTY_MAP[property](aunt[property], value):
                return False
    return True


@time_it
def main(data_lines: list[str]) -> None:
    mfcsam = get_mfcsam(MFCSAM)
    # pprint(mfcsam)

    aunts = get_aunts(data_lines)
    # pprint(aunts)

    filtered = [aunt for aunt in aunts if filter_aunts(aunt, mfcsam)]
    pprint(filtered)

    # print(f'End result: {filtered[0]["num"]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 260
    #   Finished 'main' in 1 millisecond

    # mfcsam = get_mfcsam(MFCSAM)
    # print(filter_aunts({'cats': 8, 'num': 500, 'pomeranians': 2, 'vizslas': 0}, mfcsam))
    # print(filter_aunts({'cars': 2, 'num': 212, 'pomeranians': 10, 'trees': 1}, mfcsam))

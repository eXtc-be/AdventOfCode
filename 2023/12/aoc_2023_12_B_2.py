# aoc_2023_12_B_2.py - Day 12: Hot Springs - part 2
# Before processing a line, expand it. Then, for each row, count all the different arrangements
# of operational and broken springs that meet the given criteria. What is the sum of those counts?
# adding caching to the get_combos function in the hope it is enough to finish the program in a reasonable time
# https://adventofcode.com/2023/day/12


from aoc_2023_12_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_records,
)

from tools import time_it

from pprint import pprint


cache = {}
cache_hits = 0


def get_combos(cfg: str, nums: tuple[int, ...]) -> int:
    global cache, cache_hits

    if (cfg, nums) in cache:
        cache_hits += 1
        return cache[cfg, nums]

    if cfg == '':  # no more springs to check
        return 1 if nums == () else 0  # if there are still numbers left, this branch didn't work out, so return 0

    if nums == ():  # no more numbers to check
        return 0 if "#" in cfg else 1  # if there are still # left, this branch didn't work out, so return 0

    result = 0

    if cfg[0] in '.?':  # if the first character is a working spring (or an unknown posing as a working spring)
        result += get_combos(cfg[1:], nums)  # go check the rest of the cfg string

    if cfg[0] in '#?':  # if the first character is a defective spring (or an unknown posing as a defective spring)
        if (
                nums[0] <= len(cfg) and  # are there enough characters left to create a group of length num[0]
                '.' not in cfg[:nums[0]] and  # can't have a working spring in the next num[0] characters
                (
                        nums[0] == len(cfg) or  # current group goes to the end of the cfg string
                        cfg[nums[0]] != '#'  # character after group cannot be #
                )
        ):
            # go check the rest of the cfg string (skipping the character right after the current group)
            result += get_combos(cfg[nums[0] + 1:], nums[1:])

    cache[cfg, nums] = result

    return result


def unfold_records(records: list[tuple[str, tuple[int, ...]]]) -> list[tuple[str, tuple[int, ...]]]:
    unfolded_records = []

    for cfg, nums in records:
        unfolded_records.append(('?'.join([cfg] * 5), nums * 5))

    return unfolded_records


@time_it
def main(data_lines: list[str]) -> None:
    records = create_records(data_lines)
    # pprint(records)

    unfolded_records = unfold_records(records)
    # pprint(unfolded_records)

    total = 0
    for record in unfolded_records:
        # cfg, nums = record
        # combos = get_combos(cfg, nums)
        combos = get_combos(*record)
        # print(combos)
        # print(record, combos)
        total += combos
        # total += combos

    print(f'End result: {total}')
    print(f'{len(cache)} results were cached, for a total of {cache_hits} cache hits')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 525152
    #   Finished 'main' in 1 millisecond
    #   467 results were cached, for a total of 108 cache hits
    # using input data:
    #   End result: 17391848518844
    #   Finished 'main' in 380 milliseconds
    #   251514 results were cached, for a total of 117518 cache hits

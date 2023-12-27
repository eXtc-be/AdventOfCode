# aoc_2023_12_A_4.py - Day 12: Hot Springs - part 1
# For each row, count all the different arrangements of operational and broken springs
# that meet the given criteria. What is the sum of those counts?
# fourth version: recursion!
# https://adventofcode.com/2023/day/12


from aoc_2023_12_A_1 import (
    DATA_PATH,
    load_data,
    create_records,
)

from tools import time_it

from pprint import pprint


def get_combos(cfg: str, nums: tuple[int, ...]) -> int:
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

    return result



test_data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    records = create_records(data_lines)
    # pprint(records)

    total = 0
    for record in records:
        # cfg, nums = record
        # combos = get_combos(cfg, nums)
        combos = get_combos(*record)
        # print(combos)
        # print(record, combos)
        total += combos
        # total += combos

    print(f'End result: {total}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 21
    #   Finished 'main' in 0 milliseconds
    # using input data:
    #   End result: 7047
    #   Finished 'main' in 30 milliseconds

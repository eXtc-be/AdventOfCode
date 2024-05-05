# aoc_2023_12_B_1.py - Day 12: Hot Springs - part 2
# Before processing a line, expand it. Then, for each row, count all the different arrangements
# of operational and broken springs that meet the given criteria. What is the sum of those counts?
# https://adventofcode.com/2023/day/12
# using the recursive get_combos function from aoc_2023_12_A_4, the unfolded example records
#   finished in little over one second.
# processing the input file takes way longer: the first 4 lines out of 1000 took about 15 minutes,
#   so time for another optimization


from aoc_2023_12_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_records,
)

from aoc_2023_12_A_4 import (
    get_combos
)

from tools import time_it

from pprint import pprint


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


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 525152
    #   Finished 'main' in 1 second
    # using input data:
    #   End result: ???
    #   Finished 'main' in INTERRUPTED - first 4 lines out of 1000 took about 15 minutes

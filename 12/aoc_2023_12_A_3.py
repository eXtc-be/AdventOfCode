# aoc_2023_12_A_3.py - Day 12: Hot Springs - part 1
# For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
# third version:
#   get_combos now only checks 'viable' combinations, i.e. where the number of # (after injecting the combo)
#       is equal to the sum of numbers
#   get_combos also does all the checking and injecting locally instead of calling another function (in another file!)
#   also in the old version _inject_combo was called several times, now the injection of the combo happens only once
#       per loop and locally
# https://adventofcode.com/2023/day/12


from aoc_2023_12_A_1 import (
    DATA_PATH,
    load_data,
    create_records,
)

from itertools import product

from tools import time_it

from pprint import pprint


combos_skipped = 0
total_combos = 0


def get_combos(conditions: str, numbers: list[int]) -> int:
    global combos_skipped, total_combos

    combos = 0

    for combo in product('.#', repeat=conditions.count('?')):
        total_combos += 1

        # inject combo into conditions
        i = iter(combo)
        attempt = ''.join(next(i) if char == '?' else char for char in list(conditions))

        if attempt.count('#') != sum(numbers):
            combos_skipped += 1
            continue

        groups = [group for group in attempt.split('.') if group]  # get non-empty groups

        if len(groups) != len(numbers):
            continue

        if any(group.count('#') != number for group, number in zip(groups, numbers)):
            continue

        combos += 1

    return combos


test_data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".splitlines()


@time_it
def main():
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    records = create_records(data_lines)
    # pprint(records)

    total = 0
    for record in records:
        conditions, numbers = record
        combos = get_combos(conditions, numbers)
        # print(combos)
        # print(record, combos)
        total += combos
        # total += combos

    print(f'End result: {total}')
    print(f'{combos_skipped} out of {total_combos} combinations were skipped')


if __name__ == "__main__":
    main()
    # using test_data:
    #   End result: 21
    #   Finished 'main' in 0.002 seconds
    # using input data:
    #   End result: 7047
    #   Finished 'main' in 15.765 seconds
    # using input data, without counting skipped combos:
    #   End result: 7047
    #   Finished 'main' in 15.109 seconds

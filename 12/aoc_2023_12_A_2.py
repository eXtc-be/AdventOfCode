# aoc_2023_12_A_2.py - Day 12: Hot Springs - part 1
# For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
# second version:
#   process_record now returns number of valid combos instead of the list of valid combos
#   _get_combos now looks at every group separately and multiplies each group's number of valid combinations
#       to get the total of valid combinations if the number of contiguous groups of ? or # is equal to
#       the number of numbers for that line, else if there are more or less groups,
#       it falls back on the previous strategy of trying every combination possible
# turns out this doesn't work as expected:
#   for example, using this strategy for ??.???.#?? 1,1,2 we get 2*3*2 = 12,
#       while using the old strategy we got
#           ['...#.#.##.', '.#...#.##.', '.#..#..##.', '.#.#...##.', '#....#.##.', '#...#..##.', '#..#...##.'] = 7
# https://adventofcode.com/2023/day/12


from aoc_2023_12_A_1 import(
    DATA_PATH,
    load_data,
    create_records,
    _inject_combo,
    _get_combos as _get_all_combos,
)

from itertools import product
from operator import mul
from functools import reduce

from tools import time_it

from pprint import pprint


optimized = 0


def _get_combos(conditions: str, numbers: list[int]) -> int:
    global optimized

    groups = [group for group in conditions.split('.') if group]  # get non-empty groups
    if len(groups) == len(numbers):
        '''
        optimized case where the number of groups is equal to the number of numbers
        so, instead of checking 2 to the power of the number of total ? combinations,
        we only check the sum of 2 to the power of the number of ? for each group
            2^(n+m+l) >> 2^n + 2^m + 2^l 
            e.g. for ??.??.?? 2^6 = 64 >> 2^2 + 2^2 + 2^2 = 12
        '''
        combos = []
        optimized += 1
        for group, number in zip(groups, numbers):
            if '?' in group:
                combos.append(len([
                    _inject_combo(group, combo)
                    for combo in product('.#', repeat=group.count('?'))
                    if _inject_combo(group, combo).count('#') == number
                ]))
        return reduce(mul, combos, 1)
    else:
        # fall back to checking all combinations
        return len(_get_all_combos(conditions, numbers))



def process_record(record: tuple[str, list[int]]) -> int:
    conditions, numbers = record

    combos = _get_combos(conditions, numbers)

    return combos


test_data = """
??.???.#?? 1,1,2
""".splitlines()


@time_it
def main():
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    records = create_records(data_lines)
    # pprint(records)

    total = 0
    for record in records:
        combos = process_record(record)
        print(combos)
        # print(record, combos)
        total += combos

    print(f'End result: {total}')
    print(f'{optimized} out of {len(records)} records were running the optimized branch')


if __name__ == "__main__":
    main()
    # using test_data:
    #   End result: 21
    #   Finished 'main' in 0.002 seconds
    # using input data:
    #   End result:
    #   Finished 'main' in

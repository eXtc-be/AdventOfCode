# aoc_2023_12_A_2.py - Day 12: Hot Springs - part 1
# For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
# first version: generating all possible combinations and check if they match the numbers
# https://adventofcode.com/2023/day/12

from itertools import product

from tools import time_it

from pprint import pprint

DATA_PATH = './input_2023_12'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_records(data_lines: list[str]) -> list[tuple[str, list[int]]]:
    return [(line.split()[0], [int(num) for num in line.split()[1].split(',')]) for line in data_lines if line]


def _valid_combo(conditions: str, numbers: list[int]) -> bool:
    groups = [group for group in conditions.split('.') if group]  # get non-empty groups

    if len(groups) != len(numbers):
        return False

    for group, number in zip(groups, numbers):
        if group.count('#') != number:
            return False

    return True


def _inject_combo(string: str, characters: list[str]):
    """replace all ? in string with characters"""
    i = iter(characters)
    return ''.join(next(i) if char == '?' else char for char in list(string))


def _get_combos(conditions: str, numbers: list[int]) -> list[str]:
    return [
        _inject_combo(conditions, combo)
        for combo in product('.#', repeat=conditions.count('?'))
        if _valid_combo(_inject_combo(conditions, combo), numbers)
    ]


def process_record(record: tuple[str, list[int]]) -> list[str]:
# def process_record(record: tuple[str, list[int]]) -> int:
    conditions, numbers = record

    combos = _get_combos(conditions, numbers)

    return combos
    # return len(combos)


test_data = """
??.???.#?? 1,1,2
""".splitlines()


# test_data = """
# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# """.splitlines()


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
        # print(len(combos))
        # print(record, len(combos))
        print(record, combos, len(combos))
        total += len(combos)

    print(f'End result: {total}')


if __name__ == "__main__":
    main()
    # using test_data:
    #   End result: 21
    #   Finished 'main' in 0.002 seconds
    # using input data:
    #   End result: 7047
    #   Finished 'main' in 18.477 seconds

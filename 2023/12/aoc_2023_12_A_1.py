# aoc_2023_12_A_1.py - Day 12: Hot Springs - part 1
# For each row, count all the different arrangements of operational and broken springs
# that meet the given criteria. What is the sum of those counts?
# https://adventofcode.com/2023/day/12
# first version: generating all possible combinations and check if they match the numbers

from itertools import product

from tools import time_it

from pprint import pprint

DATA_PATH = './input_2023_12'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def create_records(data_lines: list[str]) -> list[tuple[str, tuple[int, ...]]]:
    return [(line.split()[0], tuple([int(num) for num in line.split()[1].split(',')])) for line in data_lines if line]


def _valid_combo(cfg: str, nums: tuple[int, ...]) -> bool:
    groups = [group for group in cfg.split('.') if group]  # get non-empty groups

    if len(groups) != len(nums):
        return False

    for group, number in zip(groups, nums):
        if group.count('#') != number:
            return False

    return True


def _inject_combo(string: str, characters: list[str]):
    """replace all ? in string with characters"""
    i = iter(characters)
    return ''.join(next(i) if char == '?' else char for char in list(string))


def _get_combos(cfg: str, nums: tuple[int, ...]) -> list[str]:
    return [
        _inject_combo(cfg, combo)
        for combo in product('.#', repeat=cfg.count('?'))
        if _valid_combo(_inject_combo(cfg, combo), nums)
    ]


def process_record(record: tuple[str, tuple[int, ...]]) -> list[str]:
# def process_record(record: tuple[str, list[int]]) -> int:
    cfg, nums = record

    combos = _get_combos(cfg, nums)

    return combos
    # return len(combos)


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
        combos = process_record(record)
        print(len(combos))
        # print(record, len(combos))
        # print(record, combos, len(combos))
        total += len(combos)

    print(f'End result: {total}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 21
    #   Finished 'main' in 3 milliseconds
    # using input data:
    #   End result: 7047
    #   Finished 'main' in 18 seconds

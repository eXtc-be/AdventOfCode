# aoc_2024_05_B_1.py - Day 5: Print Queue - part 2
# Find the updates which are not in the correct order. What do you get if you
# add up the middle page numbers after correctly ordering just those updates?
# https://adventofcode.com/2024/day/5


from aoc_2024_05_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    read_data,
    check_update,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


def sort_update(update: list[int], rules: list[tuple[int, int]]) -> list[int]:
    sorted_update = [page for page in update]

    while True:
        finished = True
        for f, l in rules:
            if f in sorted_update and l in sorted_update:
                if sorted_update.index(f) > sorted_update.index(l):
                    sorted_update[sorted_update.index(f)], sorted_update[sorted_update.index(l)] = sorted_update[sorted_update.index(l)], sorted_update[sorted_update.index(f)]
                    finished = False
                    break
        if finished:
            break

    return sorted_update


@time_it
def main(data_lines: list[str]) -> None:
    rules, updates = read_data(data_lines)
    # print(rules)
    # print(updates)

    # print(sort_update(updates[5], rules))

    result = 0
    for update in updates:
        result += sort_update(update, rules)[len(update) // 2] if not check_update(update, rules) else 0

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 123
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4681
    #   Finished 'main' in 325 milliseconds

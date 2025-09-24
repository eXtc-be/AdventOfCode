# aoc_2024_05_A_1.py - Day 5: Print Queue - part 1
# Determine which updates are already in the correct order. What do you get
# if you add up the middle page number from those correctly-ordered updates?
# https://adventofcode.com/2024/day/5


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2024_05'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def read_data(data_lines: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    pages = []

    mode = 'r'  # start reading rules
    for line in data_lines:
        if line == '':
            mode = 'u'  # switch to reading updates
            continue

        if mode == 'r':
            rules.append(tuple([int(part) for part in line.split('|')]))
        elif mode == 'u':
            pages.append([int(part) for part in line.split(',')])

    return rules, pages


def check_update(update: list[int], rules: list[tuple[int, int]]) -> bool:
    for f, l in rules:
        if f in update and l in update:
            if update.index(f) > update.index(l):
                return False

    return True


test_data = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    rules, updates = read_data(data_lines)
    # print(rules)
    # print(updates)

    result = 0
    for update in updates:
        # print(update, check_update(update, rules))
        result += update[len(update) // 2] if check_update(update, rules) else 0

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 143
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 5091
    #   Finished 'main' in 24 milliseconds

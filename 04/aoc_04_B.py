# aoc_04_B.py - Day 4: Scratchcards  - part 2
# <description>
# https://adventofcode.com/2023/day/4


from aoc_04_A import (
    DATA_PATH,
    load_data,
    test_data,
    get_numbers,
    find_winning_numbers,
)


def get_number_of_winning_numbers(winning_numbers):
    return [[card, len(winning)] for card, winning in winning_numbers]


def _calc_line(winning_numbers_numbers, card, number):
    total = 1  # current card
    extra_cards = winning_numbers_numbers[card:card+number]  # card-1+1:card-1+number+1
    for extra_card, extra_number in extra_cards:
        total += (_calc_line(winning_numbers_numbers, extra_card, extra_number))
    return total


def calc_totals(winning_numbers_numbers):
    total = 0
    for card, number in winning_numbers_numbers:
        total += (_calc_line(winning_numbers_numbers, card, number))
    return total


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    numbers = get_numbers(data_lines)
    print(numbers)

    winning_numbers = find_winning_numbers(numbers)
    print(winning_numbers)

    winning_numbers_numbers = get_number_of_winning_numbers(winning_numbers)
    print(winning_numbers_numbers)

    total = calc_totals(winning_numbers_numbers)
    print(total)

    # print(f'End result: {sum(<last_array>)}')

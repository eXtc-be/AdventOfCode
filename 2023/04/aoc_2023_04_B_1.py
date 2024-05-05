# aoc_2023_04_B_1.py - Day 4: Scratchcards - part 2
# Process all the original and copied scratchcards until no more scratchcards are won.
# Including the original set of scratchcards, how many total scratchcards do you end up with?
# https://adventofcode.com/2023/day/4


from aoc_2023_04_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_numbers,
    find_winning_numbers,
)

from tools import time_it

# other imports

from pprint import pprint


def get_number_of_winning_numbers(winning_numbers: list[tuple[int, list[int]]]) -> list[tuple[int, int]]:
    return [(card, len(winning)) for card, winning in winning_numbers]


def _calc_line(winning_numbers_numbers: list[tuple[int, int]], card: int, number: int) -> int:
    total = 1  # current card

    extra_cards = winning_numbers_numbers[card:card+number]  # card-1+1:card-1+number+1
    for extra_card, extra_number in extra_cards:
        total += (_calc_line(winning_numbers_numbers, extra_card, extra_number))

    return total


def calc_totals(winning_numbers_numbers: list[tuple[int, int]]) -> int:
    total = 0

    for card, number in winning_numbers_numbers:
        total += (_calc_line(winning_numbers_numbers, card, number))

    return total


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    numbers = get_numbers(data_lines)
    # print(numbers)

    winning_numbers = find_winning_numbers(numbers)
    # print(winning_numbers)

    winning_numbers_numbers = get_number_of_winning_numbers(winning_numbers)
    # print(winning_numbers_numbers)

    print(f'End result: {calc_totals(winning_numbers_numbers)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 30
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 15455663
    #   Finished 'main' in 3.6 seconds

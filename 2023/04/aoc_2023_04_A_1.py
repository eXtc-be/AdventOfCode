# aoc_2023_04_A_1.py - Day 4: Scratchcards - part 1
# Take a seat in the large pile of colorful cards. How many points are they worth in total?
# https://adventofcode.com/2023/day/4


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_04'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_numbers(data_lines: list[str]) -> list[tuple[int, list[int], list[int]]]:
    numbers = []

    for line in data_lines:
        winning, own = line.split('|')
        card, winning = winning.split(':')
        card = int(card.split()[-1])
        winning = [int(number) for number in winning.split()]
        own = [int(number) for number in own.split()]
        numbers.append((card, winning, own))

    return numbers


def find_winning_numbers(numbers: list[tuple[int, list[int], list[int]]]) -> list[tuple[int, list[int]]]:
    winning_numbers = []

    for card, winning, own in numbers:
        card_winning_numbers = []
        for number in own:
            if number in winning:
                card_winning_numbers.append(number)
        winning_numbers.append((card, card_winning_numbers))

    return winning_numbers


def calc_card_scores(winning_numbers: list[tuple[int, list[int]]]) -> list[tuple[int, int]]:
    card_scores = []

    for card, numbers in winning_numbers:
        card_scores.append((card, 2 ** (len(numbers) - 1))) if numbers else 0

    return card_scores


test_data = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    numbers = get_numbers(data_lines)
    # print(numbers)

    winning_numbers = find_winning_numbers(numbers)
    # print(winning_numbers)

    card_scores = calc_card_scores(winning_numbers)
    # print(card_scores)

    print(f'End result: {sum(score for _, score in card_scores)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 13
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 23678
    #   Finished 'main' in 2 milliseconds

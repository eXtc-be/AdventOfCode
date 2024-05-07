# aoc_2023_07_B_1.py - Day 7: Camel Cards - part 2
# Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
# https://adventofcode.com/2023/day/7


from aoc_2023_07_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    Hand,
    Type,
)

from tools import time_it

from enum import IntEnum, auto
from collections import Counter

from pprint import pprint


class Card(IntEnum):
    JOKER = 1
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()


card_to_Card = {
    '2': Card.TWO,
    '3': Card.THREE,
    '4': Card.FOUR,
    '5': Card.FIVE,
    '6': Card.SIX,
    '7': Card.SEVEN,
    '8': Card.EIGHT,
    '9': Card.NINE,
    'T': Card.TEN,
    'J': Card.JOKER,
    'Q': Card.QUEEN,
    'K': Card.KING,
    'A': Card.ACE,
}


class Hand_J(Hand):
    @staticmethod
    def _get_type(cards: list[Card]) -> Type:
        # override method: replace JOKER cards with whatever card(s) make(s) this hand better,
        # then call parent method (with new cards) to determine type

        replacement = None

        if Card.JOKER in cards:
            # count how many times each card (except Jokers) is in the hand
            counter = Counter(card for card in cards if card is not Card.JOKER)

            # turns out all cases result in replacing Jokers with the same value: counter.most_common()[0][0]
            #   (except if all cards are Jokers, see below)
            # if counter.most_common()[0][1] in (4, 3, 2, 1):
            #     # Four of a kind + 1 Joker -> replace the Joker with the same card to get Five of a kind
            #     # Three of a kind + 2 Jokers -> replace Jokers with the same card to get Five of a kind
            #     # Three of a kind + 1 joker + 1 other card -> replace Joker with the same card to get Four of a kind
            #     # 2 pairs + 1 Joker -> replace Joker with any of the pairs to get Full house
            #     # 1 pair and 1-3 Jokers -> replace Joker(s) with the same card
            #     #   to get Five of a kind, Four of a kind or Three of a kind
            #     #   (it is not possible to get Full house in case of 1 Joker + 1 pair + 2 other cards)
            #     # no card appears more than once -> replace Joker(s) with any of the other cards
            #     replacement = counter.most_common()[0][0]

            if counter:
                replacement = counter.most_common()[0][0]
            else:  # original cards are all jokers -> replace them with the highest possible card
                replacement = Card.ACE

        # determine type with optimized card set (keep original cards for comparison when types are the same)
        return Hand._get_type([replacement if card == Card.JOKER else card for card in cards])


def _create_cards(hand_string: str) -> list[Card]:  # cannot import from other file, because the wrong card_to_Card would be used
    return [card_to_Card[card] for card in hand_string]


def create_hands(data_lines: list[str]) -> list[Hand_J]:  # cannot import from other file, because the wrong card_to_Card would be used
    return [
        Hand_J(
            _create_cards(line.strip().split()[0]),
            int(line.strip().split()[1]))
        for line in data_lines
    ]


test_data_2 = """
AAAAJ 0
AAAKJ 0
AAKKJ 0
AAKQJ 0
AKQTJ 0
""".strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    hands = create_hands(data_lines)
    # pprint(hands)
    # print('-' * 100)

    hands.sort()
    # pprint(hands)
    # print('-' * 100)

    # for rank, hand in enumerate(hands, 1):
    #     print(f'{rank:4d} * {hand.bid:3d} = {rank * hand.bid:8,d}')
    # print('-' * 21)
    # print(f'Total:   {sum(rank * hand.bid for rank, hand in enumerate(hands, 1)):12,}')

    print(f'End result: {sum(rank * hand.bid for rank, hand in enumerate(hands, 1))}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data_2)
    # main(test_data)

    # using test_data:
    #   End result: 5905
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 245576185
    #   Finished 'main' in 9 milliseconds

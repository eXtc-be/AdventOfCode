# aoc_2023_07_A_1.py - Day 7: Camel Cards - part 1
# Find the rank of every hand in your set. What are the total winnings?
# https://adventofcode.com/2023/day/7


from tools import time_it

from enum import IntEnum, auto
from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2023_07'

class Card(IntEnum):
    TWO = 2
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
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
    'J': Card.JACK,
    'Q': Card.QUEEN,
    'K': Card.KING,
    'A': Card.ACE,
}


class Type(IntEnum):
    HIGH = auto()  # high card
    PAIR1 = auto()  # 1 pair
    PAIR2 = auto()  # 2 pairs
    THREE = auto()  # three of a kind
    FULL = auto()  # full house
    FOUR = auto()  # four of a kind
    FIVE = auto()  # five of a kind


@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)
    bid: int = 0
    type: Type = field(init=False)

    def __post_init__(self) -> None:
        self.type = self._get_type(self.cards)

    @staticmethod
    def _get_type(cards: list[Card]) -> Type:
        s = set(cards)
        if len(s) == 1:  # all characters are identical, so five of a kind
            return Type.FIVE
        elif len(s) == 2:  # four of a kind, full house
            for e in s:
                if cards.count(e) == 4:  # if any of the characters in the set appears 4 times, it's four of a kind
                    return Type.FOUR
            else:
                # no need to check if any of the characters appears 3 times,
                # at this point a full house is the only possibility left
                return Type.FULL
        elif len(s) == 3:
            for e in s:
                if cards.count(e) == 3:
                    return Type.THREE  # if any of the characters in the set appears 3 times, it's three of a kind
            else:  # no need to check if any of the counts is 2, at this point 2 pairs is the only possibility left
                return Type.PAIR2
        elif len(s) == 4:  # the only possibility left at this point is 1 pair
            return Type.PAIR1
        else:  # the only possibility left at this point is a high card
            return Type.HIGH

    def __eq__(self, other: 'Hand') -> bool:
        if self.type == other.type:
            if all(self_card == other_card for self_card, other_card in zip(self.cards, other.cards)):
                return True
        return False

    def __lt__(self, other: 'Hand') -> bool:
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False
        else:  # both hands are of equal type
            for self_card, other_card in zip(self.cards, other.cards):
                if self_card < other_card:
                    return True
                elif self_card > other_card:
                    return False
                else:  # cards are equal, compare next card pair
                    continue
            # if we haven't returned any value at the end of this loop, both hands are identical
            return False


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _create_cards(hand_string: str) -> list[Card]:
    return [card_to_Card[card] for card in hand_string]


def create_hands(data_lines: list[str]) -> list[Hand]:
    return [
        Hand(
            _create_cards(line.strip().split()[0]),
            int(line.strip().split()[1]))
        for line in data_lines
    ]


test_data = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''.strip().splitlines()


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
    # main(test_data)

    # using test_data:
    #   End result: 6440
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 248217452
    #   Finished 'main' in 5 milliseconds

    # for hand_string in 'AAAAA AAAAK AAAKK AAAKQ AAKKQ AAKQJ AKQJT'.split():
    #     print(Hand(_create_cards(hand_string)))
    # print('-' * 100)

    # print(Hand(_create_cards('AAAAA')) > Hand(_create_cards('AAAAK')))  # True
    # print(Hand(_create_cards('AAAAA')) == Hand(_create_cards('AAAAA')))  # True
    # print(Hand(_create_cards('AAAAK')) < Hand(_create_cards('KKKKK')))  # True
    # print('-' * 100)


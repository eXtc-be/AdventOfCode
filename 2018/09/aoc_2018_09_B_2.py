# aoc_2018_09_B_2.py - Day 9: Marble Mania - part 2
# What would the new winning Elf's score be if the number of the last marble were 100 times larger?
# https://adventofcode.com/2018/day/9
# this is a complete rewrite of the original solution using a doubly linked list instead of an array


from aoc_2018_09_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_rules,
)

from tools import time_it

from dataclasses import dataclass

from pprint import pprint


BOLD = '\033[1m'
ENDC = '\033[0m'


@dataclass
class Node:
    value: int
    next: 'Node' = None
    prev: 'Node' = None

    def __str__(self) -> str:
        return f'{self.prev.value}<-{self.value}->{self.next.value}'


def draw_marbles(marbles: list[Node], current: Node, turn: int, player: int) -> None:
    global turn_len, player_len

    marble_string = ''
    marble = marbles[0]
    while True:
        if marble == current:
            marble_string += BOLD
        marble_string += f' {marble.value:{turn_len}}{ENDC}'
        marble = marble.next
        if marble == marbles[0]:
            break

    print(f'{turn:{turn_len}} [{player:{player_len}}] {marble_string}')


def do_turn(marbles: list[Node], current: Node, marble: int) -> tuple[Node, int]:
    if marble % 23 == 0:
        remove = current.prev.prev.prev.prev.prev.prev.prev
        remove.prev.next = remove.next
        remove.next.prev = remove.prev
        return remove.next, marble + remove.value
    else:
        new = Node(marble)
        new.prev = current.next.next.prev
        new.next = current.next.next
        current.next.next.prev = new
        current.next.next = new
        marbles.append(new)
        current = new
        return new, 0



turn_len = 0
player_len = 0


@time_it
def main(data: str, factor: int = 100, verbose: bool = False) -> None:
    global turn_len, player_len

    players, turns = get_rules(data)
    turns *= factor

    turn_len = len(f'{turns}')
    player_len = len(f'{players}')

    scores = [0] * players

    current = Node(0)
    current.next = current
    current.prev = current
    marbles = [current]

    if verbose:
        draw_marbles(marbles, current, 0, 0)

    for turn in range(turns):
        current, score = do_turn(marbles, current, turn + 1)
        scores[turn % players] += score
        if verbose:
            draw_marbles(marbles, current, turn + 1, turn % players + 1)
        elif turn % 1000000 == 0:
            print(f'{turn}')

    if verbose:
        print(scores)

    print(f'End result: {max(scores)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], factor=1, verbose=True)
    # for data_line in test_data:
    #     main(data_line, factor=1, verbose=False)

    # using test_data[0]:
    #   End result: 32
    #   Finished 'main' in less than a millisecond
    # using test_data[1]:
    #   End result: 8317
    #   Finished 'main' in 1 millisecond
    # using test_data[2]:
    #   End result: 146373
    #   Finished 'main' in 6 milliseconds
    # using test_data[3]:
    #   End result: 2764
    #   Finished 'main' in 1 millisecond
    # using test_data[4]:
    #   End result: 54718
    #   Finished 'main' in 5 milliseconds
    # using test_data[5]:
    #   End result: 37305
    #   Finished 'main' in 4 milliseconds
    # using input data:
    #   End result: 3352920421
    #   Finished 'main' in 8.0 seconds

    # # test marbles
    # current = Node(0)
    # current.next = current
    # current.prev = current
    # marbles = [current]
    # for marble in marbles:
    #     print(marble)
    # draw_marbles(marbles, current, 0, 0)
    #
    # new = Node(1)
    # new.prev = marbles[0]
    # new.next = marbles[0]
    # marbles[0].next = new
    # marbles[0].prev = new
    # marbles.append(new)
    # current = new
    # for marble in marbles:
    #     print(marble)
    # draw_marbles(marbles, current, 1, 1)
    #
    # new = Node(2)
    # new.prev = marbles[0]
    # new.next = marbles[1]
    # marbles[0].next = new
    # marbles[1].prev = new
    # marbles.append(new)
    # current = new
    # for marble in marbles:
    #     print(marble)
    # draw_marbles(marbles, current, 2, 2)
    #
    # new = Node(3)
    # new.prev = marbles[1]
    # new.next = marbles[0]
    # marbles[1].next = new
    # marbles[0].prev = new
    # marbles.append(new)
    # current = new
    # for marble in marbles:
    #     print(marble)
    # draw_marbles(marbles, current, 3, 3)
    #
    # new = Node(4)
    # new.prev = current.next.next.prev
    # new.next = current.next.next
    # current.next.next.prev = new
    # current.next.next = new
    # marbles.append(new)
    # current = new
    # for marble in marbles:
    #     print(marble)
    # draw_marbles(marbles, current, 4, 4)


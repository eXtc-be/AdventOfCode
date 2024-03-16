# aoc_2018_09_A_1.py - Day 9: Marble Mania - part 1
# What is the winning Elf's score?
# https://adventofcode.com/2018/day/9


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_09'

BOLD = '\033[1m'
ENDC = '\033[0m'


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_rules(data: str) -> list[int]:
    return [int(data.split()[index]) for index in (0, 6)]


def draw_marbles(marbles: list[int], current: int, turn: int, player: int) -> None:
    global turn_len, player_len
    
    marble_string = ''
    for i, marble in enumerate(marbles):
        if i == current:
            marble_string += BOLD
        marble_string += f' {marble:{turn_len}}{ENDC}'

    print(f'{turn:{turn_len}} [{player:{player_len}}] {marble_string}')


def do_turn(marbles: list[int], current: int, marble: int) -> tuple[int, int]:
    if len(marbles) < 2:
        marbles.append(marble)
        return 1, 0
    elif marble % 23 == 0:
        return (current - 7) % len(marbles), marble + marbles.pop((current - 7) % len(marbles))
    else:
        before = (current + 1) % len(marbles) + 1
        marbles.insert(before, marble)
        return before, 0


test_data = '''
9 players; last marble is worth 25 points
10 players; last marble is worth 1618 points
13 players; last marble is worth 7999 points
17 players; last marble is worth 1104 points
21 players; last marble is worth 6111 points
30 players; last marble is worth 5807 points
'''.strip().splitlines()


turn_len = 0
player_len = 0


@time_it
def main(data: str, verbose: bool = False) -> None:
    global turn_len, player_len
    
    players, turns = get_rules(data)
    # print(players, turns)
    
    turn_len = len(f'{turns}')
    player_len = len(f'{players}')
    
    # marbles = [0, 4, 2, 5, 1, 3]
    # draw_marbles(marbles, 3, 5, 5)

    # marbles = [0, 16, 8, 4, 9, 2, 10, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15]
    # draw_marbles(marbles, 1, 16, 7)

    scores = [0] * players

    marbles = [0]
    current = 0
    if verbose:
        draw_marbles(marbles, current, 0, 0)

    for turn in range(turns):
        current, score = do_turn(marbles, current, turn + 1)
        scores[turn % players] += score
        if verbose:
            draw_marbles(marbles, current, turn + 1, turn % players + 1)

    if verbose:
        print(scores)
        print(marbles)

    print(f'End result: {max(scores)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], verbose=True)
    # for data_line in test_data:
    #     main(data_line)

    # using test_data[0]:
    #   End result: 32
    #   Finished 'main' in less than a millisecond
    # using test_data[1]:
    #   End result: 8317
    #   Finished 'main' in 1 millisecond
    # using test_data[2]:
    #   End result: 146373
    #   Finished 'main' in 9 milliseconds
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
    #   End result: 398502
    #   Finished 'main' in 322 milliseconds

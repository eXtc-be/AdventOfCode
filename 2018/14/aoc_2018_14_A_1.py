# aoc_2018_14_A_1.py - Day 14: Chocolate Charts - part 1
# What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?
# https://adventofcode.com/2018/day/14


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_14'

START = [3, 7]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def do_step(board: list[int], elf_1: int, elf_2: int) -> tuple[int, int]:
    new_recipe = board[elf_1] + board[elf_2]
    for recipe in str(new_recipe):
        board.append(int(recipe))

    return (elf_1 + 1 + board[elf_1]) % len(board), (elf_2 + 1 + board[elf_2]) % len(board)


def print_board(board: list[int], elf_1: int, elf_2: int, step: int = 0) -> None:
    for i, score in enumerate(board):
        if i == elf_1:
            out = f'({score})'
        elif i == elf_2:
            out = f'[{score}]'
        else:
            out = f' {score} '
        print(out, end='')
    print()


test_data = '''
9
5
18
2018
'''.strip().splitlines()


@time_it
def main(data: str, verbose: bool = False) -> None:
    board = [score for score in START]

    recipes = int(data)

    elf_1 = 0
    elf_2 = 1

    if verbose:
        print_board(board, elf_1, elf_2)

    step = 1
    while len(board) < recipes + 10:
        elf_1, elf_2 = do_step(board, elf_1, elf_2)
        if verbose:
            print_board(board, elf_1, elf_2, step)
        step += 1

    print(f'End result: {"".join(map(str, board[recipes:recipes+10]))}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH)[0])
    main(test_data[0], verbose=True)
    # for line in test_data:
    #     print(line)
    #     main(line, verbose=False)

    # using test_data 9:
    #   End result: 5158916779
    #   Finished 'main' in less than a millisecond
    # using test_data 5:
    #   End result: 0124515891
    #   Finished 'main' in less than a millisecond
    # using test_data 18:
    #   End result: 9251071085
    #   Finished 'main' in less than a millisecond
    # using test_data 2018:
    #   End result: 5941429882
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 1741551073
    #   Finished 'main' in 1 second

# aoc_2017_17_A_1.py - Day 17: Spinlock - part 1
# What is the value after 2017 in your completed circular buffer?
# https://adventofcode.com/2017/day/17


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_17'

ROUNDS = 2017


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def do_spinlock(step: int, rounds: int = ROUNDS) -> list[int]:
    buffer = [0]
    pos = 0

    for round in range(1, rounds+1):
        if round % 10_000 == 0:
            print(f'{round:10,} {buffer[0:2]}')

        pos = (pos + step) % len(buffer) + 1
        buffer.insert(pos, round)

    return buffer


test_data = '''
3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    step = int(data_lines[0])

    buffer = do_spinlock(step)
    print(buffer)
    last_index = buffer.index(ROUNDS)

    print(f'End result: {buffer[last_index+1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 638
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 600
    #   Finished 'main' in 1 millisecond

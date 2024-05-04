# aoc_2019_16_A_1.py - Day 16: Flawed Frequency Transmission - part 1
# After 100 phases of FFT, what are the first eight digits in the final output list?
# https://adventofcode.com/2019/day/16


from tools import time_it

from itertools import cycle

from pprint import pprint


DATA_PATH = './input_2019_16'

BASE_PATTERN = [0, 1, 0, -1]

PHASES = 100


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_numbers(data: str) -> list[int]:
    return list(map(int, list(data)))


def do_phase(numbers: list[int]) -> list[int]:
    result = ''

    for i, number in enumerate(numbers, 1):
        pattern = cycle([n for n in BASE_PATTERN for _ in range(i)])
        _ = next(pattern)  # skip the very first value exactly once
        result += str(sum(num * next(pattern) for num in numbers))[-1]

    return list(map(int, list(result)))


test_data = '''
12345678
80871224585914546619083218645595
19617804207202209144916044189917
69317163492948606335995924319873
'''.strip().splitlines()


@time_it
def main(data: str, phases: int = PHASES) -> None:
    numbers = get_numbers(data)
    # pprint(numbers)

    for phase in range(phases):
        numbers = do_phase(numbers)
        # pprint(numbers)

    print(f'End result: {"".join(map(str, numbers[:8]))}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], 4)
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])

    # using test_data 0 with 4 phases:
    #   End result: 01029498
    #   Finished 'main' in less than a millisecond
    # using test_data 1 with default 100 phases:
    #   End result: 24176176
    #   Finished 'main' in 20 milliseconds
    # using test_data 2 with default 100 phases:
    #   End result: 73745418
    #   Finished 'main' in 21 milliseconds
    # using test_data 3 with default 100 phases:
    #   End result: 52432133
    #   Finished 'main' in 23 milliseconds
    # using input data:
    #   End result: 94935919
    #   Finished 'main' in 6.2 seconds

    # # for comparing the output of part 2
    # print("".join(map(str, do_phase(get_numbers('12345678'))[4:])))
    # print("".join(map(str, do_phase(get_numbers('1234567812345678'))[8:])))
    # print("".join(map(str, do_phase(get_numbers('123456781234567812345678'))[12:20])))

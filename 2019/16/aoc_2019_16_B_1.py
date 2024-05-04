# aoc_2019_16_B_1.py - Day 16: Flawed Frequency Transmission - part 2
# After repeating your input signal 10000 times and running 100 phases of FFT,
# what is the eight-digit message embedded in the final output list?
# https://adventofcode.com/2019/day/16


from aoc_2019_16_A_1 import (
    DATA_PATH,
    PHASES,
    BASE_PATTERN,
    load_data,
    # test_data,
    get_numbers,
)

from tools import time_it

# other imports

from pprint import pprint


FACTOR = 10_000


def do_phase(numbers: list[int], offset: int, factor: int = FACTOR) -> list[int]:
    running_sum = numbers.pop()
    result = str(running_sum)

    while numbers:
        running_sum = (running_sum + numbers.pop()) % 10
        result = str(running_sum) + result

    return list(map(int, list(result)))


test_data = '''
03036732577212944063491565474664
02935109699940807407585447034323
03081770884921959731165446850517
'''.strip().splitlines()


@time_it
def main(data: str, phases: int = PHASES, factor: int = FACTOR, offset: int = None) -> None:
    numbers = get_numbers(data)
    # pprint(numbers)

    if offset is None:
        offset = int(''.join(map(str, numbers[:7])))
    # print(offset)

    # calculate how much numbers we need to have at the end
    total_numbers = len(numbers) * factor
    numbers_at_end = total_numbers - offset
    # calculate how many full cycles go into numbers_at_end and how many we have to stick in front
    cycles, rest = divmod(numbers_at_end, len(numbers))
    # create the actual numbers array
    actual_numbers = ([] if rest == 0 else numbers[-rest:]) + [n for _ in range(cycles) for n in numbers]

    # print(actual_numbers)

    for phase in range(phases):
        print(phase)
        actual_numbers = do_phase(actual_numbers, offset, factor)
        # print(actual_numbers)

    print(f'End result: {"".join(map(str, actual_numbers[:8]))}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(load_data(DATA_PATH)[0], 5)  # takes 48 seconds
    # main(load_data(DATA_PATH)[0], 1)  # takes 11 seconds
    # main('12345678', 1, 1, 4)
    # main('12345678', 1, 2, 8)
    # main('12345678', 1, 2, 12)
    # main('12345678', 1, 3, 12)
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])

    # using test_data 0:
    #   End result: 84462026
    #   Finished 'main' in 1.12 seconds
    # using test_data 1:
    #   End result: 78725270
    #   Finished 'main' in 2.5 seconds
    # using test_data 2:
    #   End result: 53553731
    #   Finished 'main' in 1 second
    # using input data:
    #   End result: 24158285
    #   Finished 'main' in 16 minutes and 14 seconds

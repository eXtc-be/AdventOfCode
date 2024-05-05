# aoc_2023_06_B_1.py - Day 6: Wait For It - part 2
# How many ways can you beat the record in this one much longer race?
# https://adventofcode.com/2023/day/6
# just out of curiosity I am doing the naive (brute force) approach from aoc_2023_06_A_1
# for the part 2 race with 44_899_691 microseconds and a record of 277_113_618_901_768 millimeters


from aoc_2023_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from aoc_2023_06_A_1 import calc_distances_for_time

from tools import time_it

# other imports

from pprint import pprint


# other constants


def create_race(data_lines):
    time, distance = 0, 0

    for line in data_lines:
        if line.strip().lower().startswith('time:'):
            time = int(''.join(line.strip().split()[1:]))
        if line.strip().lower().startswith('distance:'):
            distance = int(''.join(line.strip().split()[1:]))

    return time, distance


@time_it
def main(data_lines: list[str]) -> None:
    race = create_race(data_lines)
    # print(race)

    distances = calc_distances_for_time(race[0])
    # print(distances)

    record_breakers = [distance for distance in distances if distance > race[1]]
    # print(record_breakers)

    # just show the length of the distances array
    print(f'End result: {len(record_breakers)}')  # 30125202


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 71503
    #   Finished 'main' in 11 milliseconds
    # using input data:
    #   End result: 30125202
    #   Finished 'main' in 7.8 seconds

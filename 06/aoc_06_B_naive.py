# aoc_06_B.py - Day 6: Wait For It - part 2
# use button press to beat records
# just out of curiosity I am doing the naive (brute force) approach from aoc_06_A_1
# for the part 2 race with 44_899_691 microseconds and a record of 277_113_618_901_768 millimeters
# and I'll be timing how long it takes
# https://adventofcode.com/2023/day/6


from aoc_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)
from aoc_06_A_1 import calc_distances_for_time
from aoc_06_B import create_race
from tools import convertSeconds
import time


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    race = create_race(data_lines)
    print(race)

    start_time = time.time()  # make note of start time (to calculate running time at end)

    distances = calc_distances_for_time(race[0])
    # print(distances)

    record_breakers = [distance for distance in distances if distance > race[1]]
    # print(record_breakers)

    # just show the length of the distances array
    print(f'End result: {len(record_breakers)}')  # 30125202

    print(f'finished in {convertSeconds(time.time() - start_time)}')

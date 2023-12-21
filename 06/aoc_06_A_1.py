# aoc_06_A_1.py - Day 6: Wait For It - part 1
# use button press to beat records
# naive version: loop through all possible timings and collect all results
# then compare them to the record and count how many are beating it
# https://adventofcode.com/2023/day/6


from functools import reduce
from operator import mul


DATA_PATH = './input'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def create_races(data_lines):
    for line in data_lines:
        if line.strip().lower().startswith('time:'):
            times = [int(time) for time in line.strip().split()[1:]]
        if line.strip().lower().startswith('distance:'):
            distances = [int(dist) for dist in line.strip().split()[1:]]
    return list(zip(times, distances))


def calc_distances_for_time(total_time):
    distances = []
    for button_press in range(total_time+1):
        distances.append((total_time - button_press) * button_press)
    return distances


test_data = """Time:      7  15   30
Distance:  9  40  200
""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    races = create_races(data_lines)
    # print(races)

    # distances_0 = calc_distances_for_time(races[0][0])
    # print(distances_0)
    #
    # record_breakers_0 = [distance for distance in distances_0 if distance>races[0][1]]
    # print(record_breakers_0)

    # loop through all races and remember the number of record-breaking distances
    numbers = []
    for race in races:
        print(race)
        distances = calc_distances_for_time(race[0])
        print(distances)
        record_breakers = [distance for distance in distances if distance > race[1]]
        print(record_breakers)
        print(len(record_breakers))
        numbers.append(len(record_breakers))
        print('-' * 100)
    print(numbers)

    # multiply all numbers for the end result
    print(f'End result: {reduce(mul, numbers, 1)}')

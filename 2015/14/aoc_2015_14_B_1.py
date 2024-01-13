# aoc_2015_14_B_1.py - Day 14: Reindeer Olympics - part 2
# Given the descriptions of each reindeer, after exactly 2503 seconds,
# how many points does the winning reindeer have?
# https://adventofcode.com/2015/day/14


from aoc_2015_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_reindeer_stats,
    get_distances,
    TRAVEL_TIME,
)

from tools import time_it

from collections import defaultdict

from pprint import pprint


# other constants


def get_points(seconds: int, stats: dict[str, dict[str, int]]) -> defaultdict:
    points = defaultdict(int)

    for second in range(1, seconds+1):
        distances = sorted(
            [(deer, value) for deer, value in get_distances(second, stats).items()],
            key=lambda x: x[1], reverse=True
        )
        highest = distances[0][1]
        for deer, value in distances:
            if value == highest:
                points[deer] += 1

    return points


@time_it
def main(data_lines: list[str]) -> None:
    stats = get_reindeer_stats(data_lines)
    # pprint(stats)

    # points = get_points(1000, stats)
    # pprint(points)

    points = get_points(TRAVEL_TIME, stats)
    # pprint(points)

    print(f'End result: {max(points.values())}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 689
    #   Finished 'main' in 2 milliseconds
    # using input data:
    #   End result: 1256
    #   Finished 'main' in 16 milliseconds

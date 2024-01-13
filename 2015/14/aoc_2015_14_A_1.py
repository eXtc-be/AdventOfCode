# aoc_2015_14_A_1.py - Day 14: Reindeer Olympics - part 1
# Given the descriptions of each reindeer, after exactly 2503 seconds,
# what distance has the winning reindeer traveled?
# https://adventofcode.com/2015/day/14


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2015_14'

TRAVEL_TIME = 2503


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_reindeer_stats(data_lines: list[str]) -> dict[str, dict[str, int]]:
    stats = {}
    for line in data_lines:
        deer, _, _, speed, _, _, fly_time, _, _, _, _, _, _, rest_time, _ = line.split()
        stats[deer] = {
            'speed': int(speed),
            'fly_time': int(fly_time),
            'rest_time': int(rest_time),
        }
    return stats


def _get_distances(seconds: int, stats: dict[str, int]) -> int:
    cycle_time = stats['fly_time'] + stats['rest_time']
    full_cycles, rest = divmod(seconds, cycle_time)
    last_fly = min(rest, stats['fly_time'])
    return (full_cycles * stats['fly_time'] + last_fly) * stats['speed']



def get_distances(seconds: int, stats: dict[str, dict[str, int]]) -> dict[str, int]:
    return {k: _get_distances(seconds, v) for k, v in stats.items()}


test_data = '''
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    stats = get_reindeer_stats(data_lines)
    # pprint(stats)

    # distances = get_distances(1000, stats)
    # pprint(distances)

    distances = get_distances(TRAVEL_TIME, stats)
    # pprint(distances)

    print(f'End result: {max(distances.values())}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 1120
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

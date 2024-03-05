# aoc_2018_04_A_1.py - Day 4: Repose Record - part 1
# What is the ID of the guard you chose multiplied by the minute you chose?
# https://adventofcode.com/2018/day/4


from tools import time_it

import re
from collections import defaultdict

from pprint import pprint


DATA_PATH = './input_2018_04'

EVENT_TIME = re.compile(r'\[\d+-(?P<month>\d+)-(?P<day>\d+)\s+(?P<hour>\d+):(?P<minute>\d+)\]\s+(?P<action>.+)')
EVENT_GUARD = re.compile(r'.*#(?P<guard>\d+)')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_events(data_lines: list[str]) -> dict[int, list[int]]:
    guards = defaultdict(list)
    guard = None

    for line in sorted(data_lines):
        matches = EVENT_TIME.match(line)
        if matches:
            month = int(matches.group('month'))
            day = int(matches.group('day'))
            hour = int(matches.group('hour'))
            minute = int(matches.group('minute'))
            if 'shift' in matches.group('action'):
                matches = EVENT_GUARD.match(matches.group('action'))
                if matches:
                    guard = int(matches.group('guard'))
            else:
                guards[guard].append((month, day, hour, minute))

    return guards


def get_most_sleep(guards: dict[int, list[int]]) -> tuple[int, int]:
    guard_totals = defaultdict(int)

    for guard, events in guards.items():
        current_date = (None, None)
        for event_start, event_end in zip(events[::2], events[1::2]):
            month, day, hour, minute = event_start
            guard_totals[guard] += event_end[3] - event_start[3]
            if current_date == (month, day):
                pass
            else:
                current_date = (month, day)

    return max(guard_totals.items(), key=lambda g: g[1])


def get_overlap(guards: dict[int, list[int]], guard: int) -> tuple[int, int]:
    minute_totals = defaultdict(int)

    for event_start, event_end in zip(guards[guard][::2], guards[guard][1::2]):
        for minute in range(event_start[3], event_end[3]):
            minute_totals[minute] += 1

    return max(minute_totals.items(), key=lambda m: m[1])


test_data = '''
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    guards = get_events(data_lines)
    # pprint(guards)

    guard = get_most_sleep(guards)
    print(guard)

    minute = get_overlap(guards, guard[0])
    print(minute)

    print(f'End result: {guard[0] * minute[0]}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 240
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 85296
    #   Finished 'main' in 2 milliseconds

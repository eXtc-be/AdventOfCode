# aoc_2017_24_A_4.py - Day 24: Electromagnetic Moat - part 1
# What is the strength of the strongest bridge you can make with the components you have available?
# https://adventofcode.com/2017/day/24
# after trying my hand at recursively generating valid bridges and failing miserably, I found
# a nice and fast solution on reddit that uses a defaultdict and (some kind of) linked list for the ports
# https://old.reddit.com/r/adventofcode/comments/7lte5z/2017_day_24_solutions/droveqk/


from tools import time_it

from collections import defaultdict

from pprint import pprint


DATA_PATH = './input_2017_24'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_components(data_lines: list[str]) -> defaultdict[int, set]:
    components = defaultdict(set)
    for line in data_lines:
        a, b = [int(x) for x in line.split('/')]
        components[a].add(b)
        components[b].add(a)
    return components


def bridge_generator(bridge, components):
    bridge = bridge or [(0, 0)]
    cur = bridge[-1][1]
    for b in components[cur]:
        if not ((cur, b) in bridge or (b, cur) in bridge):
            new = bridge + [(cur, b)]
            yield new
            yield from bridge_generator(new, components)


test_data = '''
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    components = get_components(data_lines)
    # pprint(components)

    # bridges = list(bridge_generator(None, components))
    # pprint(bridges)

    print(f'End result: {max(sum(sum(port for port in comp) for comp in bridge) for bridge in bridge_generator(None, components))}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 31
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1511
    #   Finished 'main' in 9.9 seconds

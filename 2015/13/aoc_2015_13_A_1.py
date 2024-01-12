# aoc_2015_13_A_1.py - Day 13: Knights of the Dinner Table - part 1
# What is the total change in happiness for the optimal seating arrangement of the actual guest list?
# https://adventofcode.com/2015/day/13


from tools import time_it

from itertools import permutations

from pprint import pprint


DATA_PATH = './input_2015_13'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _get_happinesss(guests: tuple[str, ...], map: dict[str: dict[str, int]]) -> tuple[tuple[str, ...], int]:
    distance = 0
    for guest_1, guest_2 in zip(guests, guests[1:]):
        distance += map[guest_1][guest_2]
        distance += map[guest_2][guest_1]

    distance += map[guests[0]][guests[-1]]
    distance += map[guests[-1]][guests[0]]

    return guests, distance


def get_happinesss(map: dict[str: dict[str, int]]) -> list[tuple[tuple[str, ...], int]]:
    return [_get_happinesss(combo, map) for combo in permutations(map.keys(), r=len(map.keys()))]


def get_map(data_lines: list[str]) -> dict[str: dict[str, int]]:
    map = {}

    for line in data_lines:
        src, _, oper, num, _, _, _, _, _, _, dst = line[:-1].split()
        if src not in map:
            map[src] = {}
        map[src][dst] = -int(num) if oper.lower() == 'lose' else int(num)
        if dst not in map:
            map[dst] = {}

    return map


test_data = '''
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    map = get_map(data_lines)
    # pprint(map)

    # pprint(list(permutations(map, r=len(map))))

    happiness = get_happinesss(map)
    # pprint(happiness)

    happiest = sorted(happiness, key=lambda d: d[1])[-1]
    print(f'End result: {" -> ".join(happiest[0] + happiest[0][0:1])} = {happiest[1]}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 330
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 664
    #   Finished 'main' in 88 milliseconds

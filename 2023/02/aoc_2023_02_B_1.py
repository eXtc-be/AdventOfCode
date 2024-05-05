# aoc_2023_02_B_1.py - Day 2: Cube Conundrum - part 2
# For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
# https://adventofcode.com/2023/day/2


from aoc_2023_02_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    COLORS,
    get_games,
    analyze_games,
)

from tools import time_it

from math import prod

from pprint import pprint


# other constants


def calc_powers(summary: dict[int, dict[str, int]]):
    result = {}

    for game_id, cubes in summary.items():
        result[game_id] = prod(cubes.values())

    return result


@time_it
def main(data_lines: list[str]) -> None:
    games = get_games(data_lines)
    # pprint(games)

    summary = analyze_games(games)
    # pprint(summary)

    powers = calc_powers(summary)
    # print(powers)

    print(f'End result: {sum(powers.values())}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 2286
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 65371
    #   Finished 'main' in 1 millisecond

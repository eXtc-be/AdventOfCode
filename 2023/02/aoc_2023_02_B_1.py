# aoc_2023_02_B_1.py - Day 2: Cube Conundrum - part 2
# calculate the 'power' of combinations
# https://adventofcode.com/2023/day/2


from aoc_2023_02_A import (
    DATA_PATH,
    load_data,
    test_data,
    colors,
    split_data,
    summarize_data,
)

from math import prod


def calc_powers(summary):
    result = {}
    for id_, color_values in summary.items():
        result[id_] = prod(color_values.values())
    return result


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    print(data_lines)

    data = split_data(data_lines)
    print(data)

    summary = summarize_data(data)
    print(summary)

    powers = calc_powers(summary)
    print(powers)

    print(f'End result: {sum(powers.values())}')

# aoc_2019_14_A_1a.py - Day 14: Space Stoichiometry - part 1
# Given the list of reactions in your puzzle input,
# what is the minimum amount of ORE required to produce exactly 1 FUEL?
# https://adventofcode.com/2019/day/14
# based on the solution from Alexandre Martins: https://asmartins.com/blog/rocket-fuel/
# this version keeps track of chemicals produced to make minimize the waste
# it also always takes the last element from the needed list
# the result: all test cases pass with correct answers, but running the real data gives a result that is too high


from aoc_2019_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

from collections import defaultdict
import math

from pprint import pprint


# other constants


def parse_chemical(string: str) -> tuple[int, str]:
    return int(string.split()[0]), string.split()[1]


def get_reactions(data_lines: list[str]) -> dict[str, tuple[int, list[tuple[int, str]]]]:
    reactions = {}

    for line in data_lines:
        input_specs, output_spec = line.split(' => ')
        amount, name = parse_chemical(output_spec)
        reactions[name] = (amount, [parse_chemical(input_spec) for input_spec in input_specs.split(', ')])

    return reactions


def ore_required(reactions: dict[str, tuple[int, list[tuple[int, str]]]], goal: tuple[int, str]):
    ore = 0

    needs = defaultdict(int, {goal[1]: goal[0]})
    stock = defaultdict(int)

    iterations = 0
    while needs:
        iterations += 1

        chemical, required = needs.popitem()  # removes an item from the right

        quantity = required
        in_stock = stock[chemical]  # retrieve previous stock, or create new entry with quantity=0
        quantity -= in_stock
        stock[chemical] = abs(quantity) if quantity < 0 else 0

        required -= in_stock - stock[chemical]

        produced, ingredients = reactions[chemical]
        n = math.ceil(required / produced)
        stock[chemical] = produced * n - required

        for quantity, ingredient in ingredients:
            if ingredient == 'ORE':
                ore += quantity * n
            else:
                needs[ingredient] += quantity * n

    return ore, iterations


@time_it
def main(data_lines: list[str]) -> None:
    reactions = get_reactions(data_lines)
    # pprint(reactions)

    ore, iterations = ore_required(reactions, (1, 'FUEL'))

    print(f'End result: {ore} ({iterations} iterations)')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])

    # using test_data 0:
    #   End result: 31 (6 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 165 (10 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 13312 (16 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 3:
    #   End result: 180697 (27 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 4:
    #   End result: 2210736 (66 iterations)
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 663053 (792 iterations) - too high
    #   Finished 'main' in 1 millisecond

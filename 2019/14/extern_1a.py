# extern_1a.py
# https://asmartins.com/blog/rocket-fuel/
# base program


from aoc_2019_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from tools import time_it

from collections import defaultdict
import math

from pprint import pprint


def parse_chemical(string):
    return int(string.split()[0]), string.split()[1]


def get_reactions(data_lines):
    reactions = {}

    for line in data_lines:
        input_specs, output_spec = line.split(' => ')
        amount, name = parse_chemical(output_spec)
        reactions[name] = (amount, [parse_chemical(input_spec) for input_spec in input_specs.split(', ')])

    return reactions


def ore_required_stock(reactions, qty):
    ore_required = 0
    needs = defaultdict(int, {'FUEL': qty})
    stock = defaultdict(int)

    def get_from_stock(qty, chemical):
        in_stock = stock[chemical]
        qty -= in_stock
        stock[chemical] = abs(qty) if qty < 0 else 0
        return in_stock - stock[chemical]

    iterations = 0
    while needs:
        iterations += 1
        chemical, qty_required = needs.popitem()
        from_store = get_from_stock(qty_required, chemical)
        qty_required -= from_store
        qty_produced, ingredients = reactions[chemical]
        n = math.ceil(qty_required/qty_produced)
        stock[chemical] = qty_produced*n - qty_required
        for qty_ingredient, ingredient in ingredients:
            if ingredient == 'ORE':
                ore_required += qty_ingredient*n
            else:
                needs[ingredient] += qty_ingredient*n

    return ore_required, iterations


@time_it
def main(data_lines: list[str]) -> None:
    reactions = get_reactions(data_lines)
    # pprint(reactions)

    ore_required, iterations = ore_required_stock(reactions, 1)

    print(f'End result: {ore_required} ({iterations} iterations)')


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


# extern_1b.py
# https://asmartins.com/blog/rocket-fuel/
# optimized


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


def topological_order(reactions):
    visited_nodes = []
    order = []

    def dfs(reactions, node):
        visited_nodes.append(node)
        if node == 'ORE':
            return
        _, ingredients = reactions[node]
        for _, ingredient in ingredients:
            if ingredient not in visited_nodes:
                dfs(reactions, ingredient)
        order.append(node)

    dfs(reactions, 'FUEL')
    order.reverse()
    order.append('ORE')
    ordering = {element: index for index, element in enumerate(order)}
    return ordering


def ore_required_topological(reactions, ordering, qty):
    ore_required = 0
    needs = defaultdict(int, {'FUEL': qty})

    iterations = 0
    while needs:
        iterations += 1
        chemical = sorted(needs.keys(), key=lambda k: ordering[k])[0]
        qty_required = needs.pop(chemical)
        qty_produced, ingredients = reactions[chemical]
        n = math.ceil(qty_required/qty_produced)
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

    ordering = topological_order(reactions)
    # pprint(ordering)

    ore_required, iterations = ore_required_topological(reactions, ordering, 1)

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
    #   End result: 165 (7 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 13312 (9 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 3:
    #   End result: 180697 (12 iterations)
    #   Finished 'main' in less than a millisecond
    # using test_data 4:
    #   End result: 2210736 (17 iterations)
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 654909 (60 iterations)
    #   Finished 'main' in less than a millisecond


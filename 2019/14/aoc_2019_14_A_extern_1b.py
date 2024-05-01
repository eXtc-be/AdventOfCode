# aoc_2019_14_A_1.py - Day 14: Space Stoichiometry - part 1
# Given the list of reactions in your puzzle input,
# what is the minimum amount of ORE required to produce exactly 1 FUEL?
# https://adventofcode.com/2019/day/14
# based on the solution from Alexandre Martins: https://asmartins.com/blog/rocket-fuel/
# this version uses a list of topological distances for each chemical as a way to prioritize chemicals that
# are further away from FUEL. the number of iterations is greatly reduced (exponentially)
# the result: all test cases pass with correct answers, and so does running the program it with the real data


from aoc_2019_14_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
)

from aoc_2019_14_A_extern_1a import (
    get_reactions
)

from tools import time_it

from collections import defaultdict
import math

from pprint import pprint


# other constants


def order_chemicals(reactions: dict[str, tuple[int, list[tuple[int, str]]]], goal: str) -> dict[str, int]:
    visited_nodes = []
    order = []

    def dfs(reactions: dict[str, tuple[int, list[tuple[int, str]]]], node: str):
        visited_nodes.append(node)
        if node == 'ORE':
            return

        _, ingredients = reactions[node]
        for _, ingredient in ingredients:
            if ingredient not in visited_nodes:
                dfs(reactions, ingredient)

        order.append(node)

    dfs(reactions, goal)
    order.reverse()
    order.append('ORE')
    ordering = {element: index for index, element in enumerate(order)}
    return ordering


def ore_required(
        reactions: dict[str, tuple[int, list[tuple[int, str]]]],
        ordering: dict[str, int],
        goal: tuple[int, str]
):
    ore = 0

    needs = defaultdict(int, {goal[1]: goal[0]})

    iterations = 0
    while needs:
        iterations += 1

        # order chemicals by topological order and pick the one furthest from the FUEL
        chemical = sorted(needs.keys(), key=lambda k: ordering[k])[0]
        required = needs.pop(chemical)  # get selected chemical's required amount

        produced, ingredients = reactions[chemical]
        n = math.ceil(required / produced)

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

    ordering = order_chemicals(reactions, 'FUEL')
    # pprint(ordering)

    ore, iterations = ore_required(reactions, ordering, (1, 'FUEL'))

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
    #   End result: 654909 (60 iterations) - too high
    #   Finished 'main' in less than a millisecond

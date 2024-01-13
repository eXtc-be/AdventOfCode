# aoc_2015_15_A_1.py - Day 15: Science for Hungry People - part 1
# Given the ingredients in your kitchen and their properties,
# what is the total score of the highest-scoring cookie you can make?
# https://adventofcode.com/2015/day/15


from tools import time_it

from itertools import combinations_with_replacement
from collections import Counter
from functools import reduce
from operator import mul

from pprint import pprint


DATA_PATH = './input_2015_15'

PROPERTIES = 'capacity durability flavor texture'.split()


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_ingredients(data_lines: list[str]) -> dict[str, dict[str, int]]:
    ingredients: dict[str, dict[str, int]] = {}

    for line in data_lines:
        ingredient, properties = line.split(': ')
        properties = properties.split(', ')
        ingredients[ingredient] = {}
        for property in properties:
            prop, val = property.split()
            ingredients[ingredient][prop] = int(val)

    return ingredients


def _score_combo(combo: dict[str, int], ingredients: dict[str, dict[str, int]]) -> int:
    scores = []

    for property in PROPERTIES:
        score = 0
        for ingredient in combo:
            score += ingredients[ingredient][property] * combo[ingredient]
        if score > 0:
            scores.append(score)
        else:
            return 0

    return reduce(mul, scores, 1)


def get_combos(ingredients: dict[str, dict[str, int]], number: int) -> list[dict[str, int]]:
    combos: list[dict[str, int]] = []

    for combo_list in combinations_with_replacement(ingredients.keys(), number):
        counter = Counter(combo_list)
        if len(counter.keys()) == len(ingredients.keys()):  # make sure all ingredients are used (not sure if needed)
            combo = {}
            for ingredient, num in counter.items():
                combo[ingredient] = num

            combo['score'] = _score_combo(combo, ingredients)

            combos.append(combo)

    return combos


test_data = '''
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    ingredients = get_ingredients(data_lines)
    # pprint(ingredients)

    combos = get_combos(ingredients, 100)
    # pprint(combos)

    highest_score = max(combos, key=lambda c: c['score'])

    print(f'End result: {highest_score}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 62842880
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 13882464
    #   Finished 'main' in 1.18 seconds

# aoc_2015_15_B_1.py - Day 15: Science for Hungry People - part 2
# Given the ingredients in your kitchen and their properties,
# what is the total score of the highest-scoring cookie you can make with a calorie total of 500?
# https://adventofcode.com/2015/day/15


from aoc_2015_15_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_ingredients,
    get_combos
)

from tools import time_it

# other imports

from pprint import pprint


CALORIES = 500


def _calc_calories(combo: dict[str, int], ingredients: dict[str, dict[str, int]]) -> int:
    calories = 0

    for ingredient in ingredients:
        calories += ingredients[ingredient]['calories'] * combo[ingredient]

    return calories


@time_it
def main(data_lines: list[str]) -> None:
    ingredients = get_ingredients(data_lines)
    # pprint(ingredients)

    combos = get_combos(ingredients, 100)
    # pprint(combos)

    filtered_combos = [combo for combo in combos if _calc_calories(combo, ingredients) == CALORIES]
    pprint(filtered_combos)

    highest_score = max(filtered_combos, key=lambda c: c['score'])

    print(f'End result: {highest_score}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 57600000
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 11171160
    #   Finished 'main' in 1.24 seconds

    # ingredients = get_ingredients(data_lines)
    # combo = {'Butterscotch': 40, 'Cinnamon': 60}
    # print(_calc_calories(combo, ingredients))

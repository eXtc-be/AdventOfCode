# aoc_2015_19_B_1.py - Day 19: Medicine for Rudolph - part 2
# Given the available replacements and the medicine molecule in your puzzle input,
# what is the fewest number of steps to go from e to the medicine molecule?
# https://adventofcode.com/2015/day/19

# tried several strategies to no avail:
#   - brute force: trying every combination possible by doing all possible replacements
#       works well on the example data, but runs forever on the actual data
#   - same as before, but prints all winning combinations (i.e. when the target molecule is found),
#       instead of listing all winning combinations and selecting the shortest one
#       ran for a couple of hours without any result
#   - optimized brute force: by sorting the replacements by how often they appear in the
#       final molecule, and sorting the atoms by the sum of their replacement appearances,
#       I was hoping I would reach the final molecule faster, but the program ran for a couple
#       of hours without any result
#   - decided to try to deconstruct the molecule from finish to start, but couldn't find a way to do it
# I finally turned to the internet and found a working solution that used re.sub to deconstruct the molecule
#   see aoc_2015_19_B_2.py


from aoc_2015_19_A_1 import (
    DATA_PATH,
    load_data,
    get_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def _create_variations(start: list[str], target: str, replacements: dict[str, list[str]]) -> list[list[str]]:
    # create a list of all possible replacements for the current start
    candidates = []

    if start[-1] == target:
        print(start)
        return [start]

    if len(start[-1]) >= len(target):
        return []

    for atom in replacements:
        if atom in start[-1]:
            for replacement in replacements[atom]:
                idx = -1
                while True:
                    idx = start[-1].find(atom, idx + 1)
                    if idx == -1:
                        break
                    new = start[-1][:idx] + replacement + start[-1][idx + len(atom):]
                    candidate = _create_variations(start + [new], target, replacements)
                    if candidate:
                        candidates += candidate

    return candidates


def create_molecule(start: str, target: str, replacements: dict[str, list[str]]) -> list[list[str]]:
    collection = []

    for candidate in _create_variations([start], target, replacements):
        if candidate[-1] == target:
            collection.append(candidate)

    return collection


def _find_previous_molecule(start: str, target: str, replacements: dict[str, list[str]]) -> [str]:
    new_molecule = target

    for atom, replacement_list in replacements.items():
        for replacement in replacement_list:
            if replacement in target:
                idx = -1
                while True:
                    idx = new_molecule.find(replacement, idx + 1)
                    if idx == -1:
                        break
                    new_molecule = new_molecule[:idx] + atom + new_molecule[idx+len(replacement):]


def deconstruct_molecule(start: str, target: str, replacements: dict[str, list[str]]) -> list[str]:
    steps = [target]

    while steps[-1] != start:
        steps += _find_previous_molecule(steps[-1], target, replacements)

    return steps


test_data = '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    replacements, molecule = get_data(data_lines)
    # pprint(replacements)
    # print(molecule)

    # IDEA: sort each origin atom's replacement list by the number of occurrences in the final molecule and
    #       then sort the atoms by the total number of occurrences / the highest number of occurrences in the molecule
    #       this should hopefully speed up the creation of the final molecule
    #   -> did not work

    # for replaced, replacement_list in replacements.items():
    #     print(replaced)
    #     for replacement in replacement_list:
    #         print('\t', replacement, molecule.count(replacement))

    # print('-' * 100)

    for replaced, replacement_list in replacements.items():
        replacement_list.sort(key=lambda x: molecule.count(x), reverse=True)

    sorted_replacements = sorted(
        list(replacements),
        key=lambda x: sum(molecule.count(y) for y in replacements[x]),
        reverse=True
    )

    # for replacement_key in sorted_replacements:
    #     print(replacement_key)
    #     for replacement in replacements[replacement_key]:
    #         print('\t', replacement, molecule.count(replacement))

    # IDEA: start with the molecule and find as many replacements as possible / all replacements,
    #       then do the same with the simplified molecule etcera until the start molecule is reached

    steps = deconstruct_molecule('e', molecule, replacements)
    pprint(steps)

    # steps = create_molecule('e', molecule, replacements)
    # # pprint(steps)
    #
    # shortest = min(steps, key=lambda x: len(x))

    # print(f'End result: {len(shortest)-1}: {" -> ".join(shortest)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 6: e -> H -> HO -> HOO -> HOOO -> HOHHO -> HOHOHO
    #   Finished 'main' in 3 milliseconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

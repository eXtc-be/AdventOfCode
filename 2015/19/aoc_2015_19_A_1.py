# aoc_2015_19_A_1.py - Day 19: Medicine for Rudolph - part 1
# How many distinct molecules can be created after all the different ways
# you can do one replacement on the medicine molecule?
# https://adventofcode.com/2015/day/19


from tools import time_it

from collections import defaultdict
import re

from pprint import pprint


DATA_PATH = './input_2015_19'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_data(data_lines: list[str]) -> tuple[dict[str, list[str]], str]:
    replacements = defaultdict(list)
    molecule = ''

    for line in data_lines:
        if ' => ' in line:  # replacement
            origin, replacement = line.split(' => ')
            replacements[origin].append(replacement)
        else:  # molecule
            molecule = line

    return replacements, molecule


def create_molecules(molecule: str, replacements: dict[str, list[str]]) -> set[str]:
    molecules = set()

    for atom, replacement_list in replacements.items():
        if atom in molecule:
            idx = -1
            while True:
                idx = molecule.find(atom, idx+1)
                if idx == -1:
                    break
                for replacement in replacement_list:
                    molecules.add(molecule[:idx] + replacement + molecule[idx+len(atom):])

    return molecules


test_data = '''
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

    molecules = create_molecules(molecule, replacements)
    # pprint(molecules)

    print(f'End result: {len(molecules)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 7
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 576
    #   Finished 'main' in 1 millisecond

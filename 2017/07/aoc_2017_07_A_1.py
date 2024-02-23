# aoc_2017_07_A_1.py - Day 7: Recursive Circus - part 1
# What is the name of the bottom program?
# https://adventofcode.com/2017/day/7
# solution 1: finding the bottom program by grouping the top program (without any children) and checking
#             the rest of the programs if any have any of the top programs in their children list


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2017_07'

# other constants


@dataclass
class Program:
    name: str
    weight: int
    children: list[str]
    parent: 'Program' = None

    def __hash__(self):
        return hash(self.name)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_programs(datalines: list[str]) -> list[Program]:
    programs = []

    for line in datalines:
        parts = line.split(' -> ')
        name, weight = parts[0].split()
        weight = int(weight[1:-1])  # remove parentheses and convert to int
        carry = []
        if len(parts) > 1:  # this program carries other programs
            carry = parts[1].split(', ')
        programs.append(Program(name, weight, carry))

    return programs


def get_root(programs: list[Program]) -> Program:
    while len(programs) > 1:
        children = [program for program in programs if not program.children]
        children_names = [program.name for program in programs if not program.children]
        programs = [program for program in programs if program.children]

        for program in programs:
            to_remove = []
            for child_name in program.children:
                if child_name in children_names:
                    to_remove.append(child_name)
            for child_name in to_remove:
                program.children.remove(child_name)

    return programs[0]


# test_data = '''
# a (66) -> b, c
# b (57) -> d, e
# c (61) -> f, g
# d (66)
# e (57) -> h, i
# f (72)
# g (66)
# h (77)
# i (56)
# '''.strip().splitlines()

test_data = '''
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    programs = get_programs(data_lines)
    # pprint(programs)

    root = get_root(programs)
    # pprint(root)

    print(f'End result: {root.name}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: tknk
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: eugwuhl
    #   Finished 'main' in 17 milliseconds

# aoc_2017_07_A_1.py - Day 7: Recursive Circus - part 1
# What is the name of the bottom program?
# https://adventofcode.com/2017/day/7
# solution 2: finding the bottom program by making a tree structure of all nodes


from aoc_2017_07_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    Program,
    get_programs,
)

from tools import time_it

from collections import defaultdict

from pprint import pprint


# other constants


def create_tree(programs: list[Program]):
    for program in programs:
        for parent in programs:
            if program.name in parent.children:
                program.parent = parent
                break



# test_data = '''
# a (66) -> b, c
# b (57)
# c (61)
# '''.strip().splitlines()

# test_data = '''
# a (1) -> b, c
# b (2) -> d, e
# c (3) -> f, g
# d (4)
# e (5)
# f (6)
# g (7)
# '''.strip().splitlines()

# test_data = '''
# a (1) -> b, c
# b (2) -> d, e
# c (3) -> f, g
# d (4)
# e (5) -> h, i
# f (6)
# g (7)
# h (8)
# i (9)
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

    create_tree(programs)
    # pprint(programs)

    print(f'End result: {[program for program in programs if not program.parent][0].name}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: tknk
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: eugwuhl
    #   Finished 'main' in 82 milliseconds

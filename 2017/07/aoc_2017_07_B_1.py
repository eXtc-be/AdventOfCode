# aoc_2017_07_B_1.py - Day 7: Recursive Circus - part 2
# Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?
# https://adventofcode.com/2017/day/7


from aoc_2017_07_A_1 import (
    DATA_PATH,
    load_data,
    Program,
    get_programs,
)

from aoc_2017_07_A_2 import (
    test_data,
    create_tree,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def get_weight(programs: list[Program], root: Program) -> int:
    weight = 0
    if root.children:
        for child_name in root.children:
            for program in programs:
                if program.name == child_name:
                    weight += get_weight(programs, program)
                    break
    else:
        return root.weight

    return root.weight + weight


@time_it
def main(data_lines: list[str]) -> None:
    programs = get_programs(data_lines)
    # pprint(programs)

    create_tree(programs)
    # pprint(programs)

    # root = [program for program in programs if not program.parent][0]
    root = [program for program in programs if program.name == 'drjmjug'][0]

    weights = []
    for child_name in root.children:
        child = [program for program in programs if program.name == child_name][0]
        weights.append({child.name: get_weight(programs, child)})

    print(weights)

    # print(f'End result: {0}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 420
    #   found solution by calculating the weights of root's sub towers,
    #   then selecting the sub tower with different weight and calculating its subtowers
    #   until a subtower is found that has no different subtowers,
    #   then taking that subtower's weight and changing it so its total weight equals the other sub towers' weights

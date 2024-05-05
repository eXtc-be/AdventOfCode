# aoc_2023_08_A_1.py - Day 8: Haunted Wasteland - part 1
# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
# https://adventofcode.com/2023/day/8


from tools import time_it

from itertools import cycle
import re

from pprint import pprint


DATA_PATH = './input_2023_08'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_instructions(instruction_line: str) -> cycle[str]:
    return cycle(instruction_line)


def get_nodes(data_lines: list[str]) -> dict[str, dict[str, str]]:
    return {
            line.split(' = ')[0]: {
                'L': re.sub(r'[()]', '', line.split(' = ')[1]).split(', ')[0],
                'R': re.sub(r'[()]', '', line.split(' = ')[1]).split(', ')[1],
            } for line in data_lines
    }


def walk_path(instructions: cycle[str], nodes: dict[str, dict[str, str]]) -> list[str]:
    steps = ['AAA']
    current_node = nodes['AAA']
    while True:
        instruction = next(instructions)
        next_node = current_node[instruction]
        steps.append(next_node)
        current_node = nodes[next_node]
        if current_node == nodes['ZZZ']:
            break
    return steps


test_data = [
'''
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''.strip().splitlines(),
'''
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''.strip().splitlines(),
]


@time_it
def main(data_lines: list[str]) -> None:
    instructions = get_instructions(data_lines[0])
    # for i in range(10):
    #     print(next(instructions))

    nodes = get_nodes(data_lines[2:])  # skip first 2 lines
    # print(nodes)

    steps = walk_path(instructions, nodes)
    # print(steps)

    print(f'End result: {len(steps) - 1}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])

    # using test_data 0:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 16897
    #   Finished 'main' in 6 milliseconds

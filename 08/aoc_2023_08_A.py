# aoc_2023_08_A.py - Day 8: Haunted Wasteland - part 1
# follow instructions to choose the next node in a bunch of nodes and try to get to the end
# https://adventofcode.com/2023/day/8


from itertools import cycle
import re

DATA_PATH = './input_2023_08'


def load_data(path):
    with open(path) as f:
        return f.read().splitlines()


def get_instructions(instruction_line):
    return cycle(instruction_line)


def get_nodes(data_lines):
    return {
            line.split(' = ')[0]: {
                'L': re.sub(r'[()]', '', line.split(' = ')[1]).split(', ')[0],
                'R': re.sub(r'[()]', '', line.split(' = ')[1]).split(', ')[1],
            } for line in data_lines
    }


def walk_path(instructions, nodes):
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


test_data_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines()

test_data_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    # print(data_lines)

    instructions = get_instructions(data_lines[0])
    # for i in range(10):
    #     print(next(instructions))

    nodes = get_nodes(data_lines[2:])  # skip first 2 lines
    # print(nodes)

    steps = walk_path(instructions, nodes)
    # print(steps)

    print(f'End result: {len(steps) - 1}')

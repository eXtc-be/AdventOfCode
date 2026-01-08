# aoc_2023_08_B_2.py - Day 8: Haunted Wasteland - part 2
# Simultaneously start on every node that ends with A.
# How many steps does it take before you're only on nodes that end with Z?
# https://adventofcode.com/2023/day/8
# aoc_2023_08_B_1 ran for over 12 hours and didn't produce a result
# after reading some threads on reddit, I am now going to try 'Least Common Multiplier' (LCM)
# first I need to figure out the loop size for each starting node,
# then calculate the LCM of the loop sizes + the instructions length to get the final result, hopefully


from aoc_2023_08_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_nodes
)

from tools import time_it

from itertools import cycle
from math import lcm

from pprint import pprint


# other constants


def get_cycles(instruction_line: str, nodes: dict[str, dict[str, str]]):
    cycles = []
    start_nodes = {node: nodes[node] for node in nodes if node.endswith('A')}

    for node in start_nodes:
        current_cycle = [node]
        current_node = nodes[node]
        instructions = cycle(instruction_line)  # restart instructions for every start node
        while True:
            instruction = next(instructions)
            next_node = current_node[instruction]
            if next_node in current_cycle:  # we just looped
                idx = current_cycle.index(next_node)
                cycles.append(current_cycle[idx:])
                break  # while True
            current_cycle.append(next_node)
            current_node = nodes[next_node]

    return cycles


def get_cycle_lengths(instruction_line: str, nodes: dict[str, dict[str, str]]) -> list[int]:
    """does the same thing as get_cycles, but doesn't store the cycles: just keeps track of the cycle lengths"""
    cycle_lengths = []
    start_nodes = {node: nodes[node] for node in nodes if node.endswith('A')}

    for node in start_nodes:
        current_cycle = [node]  # gotta still store current cycle for testing for inclusion of next_node
        current_node = nodes[node]
        instructions = cycle(instruction_line)  # restart instructions for every start node
        while True:
            instruction = next(instructions)
            next_node = current_node[instruction]
            if next_node in current_cycle:  # we just looped
                idx = current_cycle.index(next_node)
                cycle_lengths.append(len(current_cycle) - idx)
                break  # while True
            current_cycle.append(next_node)
            current_node = nodes[next_node]

    return cycle_lengths


test_data = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    instruction_length = len(data_lines[0])
    # print(instruction_length)

    nodes = get_nodes(data_lines[2:])  # skip first 2 lines
    # print(nodes)

    # cycles = get_cycles(data_lines[0], nodes)
    # print(cycles)

    # cycle_lengths = [len(cycle) for cycle in cycles] + [instruction_length]
    # print(cycle_lengths)

    cycle_lengths = get_cycle_lengths(data_lines[0], nodes) + [instruction_length]
    # print(cycle_lengths)

    print(f'End result: {lcm(*cycle_lengths)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data storing all cycles:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using test_data storing only cycle lengths:
    #   End result: 6
    #   Finished 'main' in xxx
    # using input data storing all cycles:
    #   End result: 16563603485021
    #   Finished 'main' in 3 milliseconds
    # using input data storing only cycle lengths:
    #   End result: 16563603485021
    #   Finished 'main' in 3 milliseconds

# aoc_2023_08_B_2.py - Day 8: Haunted Wasteland - part 2
# follow instructions to choose the next node in a bunch of nodes and try to get to the end,
# but this time the start and end nodes are arrays of nodes
# so aoc_2023_08_B_1 ran for over 12 hours and did not produce a result
# after reading some threads on reddit, I am now going to try 'Least Common Multiplyer' (LCM)
# first I need to figure out the loop size for each starting node,
# then calculate the LCM of the loop sizes + the instructions length to get the final result, hopefully
# https://adventofcode.com/2023/day/8


from aoc_2023_08_A import (
    DATA_PATH,
    load_data,
    test_data_1,
    test_data_2,
    get_nodes
)

import time
from itertools import cycle
from math import lcm
from tools import convertSeconds


def get_cycles(instruction_line, nodes):
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


def get_cycle_lengths(instruction_line, nodes):
    """does not store all cycles, but just keeps track of the cycle lengths"""
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


test_data_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines()


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    # data_lines = test_data_3
    # print(data_lines)

    instruction_length = len(data_lines[0])
    print(instruction_length)

    nodes = get_nodes(data_lines[2:])  # skip first 2 lines
    # print(nodes)

    start_time = time.time()  # make note of start time (to calculate running time at end)

    cycles = get_cycles(data_lines[0], nodes)
    print(cycles)

    # cycle_lengths = [len(cycle) for cycle in cycles] + [instruction_length]
    # print(cycle_lengths)
    #
    cycle_lengths = get_cycle_lengths(data_lines[0], nodes) + [instruction_length]
    print(cycle_lengths)

    print(f'End result: {lcm(*cycle_lengths)}')

    print(f'finished in {convertSeconds(time.time() - start_time)}')

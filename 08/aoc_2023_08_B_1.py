# aoc_2023_08_B_1.py - Day 8: Haunted Wasteland - part 2
# follow instructions to choose the next node in a bunch of nodes and try to get to the end,
# but this time the start and end nodes are arrays of nodes
# https://adventofcode.com/2023/day/8


from aoc_2023_08_A import (
    DATA_PATH,
    load_data,
    test_data_1,
    test_data_2,
    get_instructions,
    get_nodes
)

import time

from tools import convertSeconds


def walk_path(instructions, nodes):
    # steps = [[node for node in nodes if node.endswith('A')]]  # keep track of all steps
    steps = 0  # keep track of number of steps
    current_nodes = {node: nodes[node] for node in nodes if node.endswith('A')}

    while True:
        instruction = next(instructions)
        next_nodes = [current_node[instruction] for current_node in current_nodes.values()]
        # steps.append(next_nodes)  # keep track of all steps
        steps += 1  # keep track of number of steps
        current_nodes = {next_node: nodes[next_node] for next_node in next_nodes}
        if all(current_node.endswith('Z') for current_node in current_nodes):
            break
    return steps


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

    instructions = get_instructions(data_lines[0])
    # for i in range(10):
    #     print(next(instructions))

    nodes = get_nodes(data_lines[2:])  # skip first 2 lines
    # print(nodes)

    start_time = time.time()  # make note of start time (to calculate running time at end)

    steps = walk_path(instructions, nodes)
    # print(steps)

    # print(f'End result: {len(steps) - 1}')
    print(f'End result: {steps}')

    print(f'finished in {convertSeconds(time.time() - start_time)}')

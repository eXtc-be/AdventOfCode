# aoc_2023_08_B_1.py - Day 8: Haunted Wasteland - part 2
# Simultaneously start on every node that ends with A.
# How many steps does it take before you're only on nodes that end with Z?
# https://adventofcode.com/2023/day/8
# despite running the program with test data took less than a millisecond, running it with the real data
# takes way too long (even when using an int instead of a list to keep track of the steps)


from aoc_2023_08_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    get_instructions,
    get_nodes,
    cycle,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def walk_path(instructions: cycle[str], nodes: dict[str, dict[str, str]]) -> int:
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
    instructions = get_instructions(data_lines[0])
    # for i in range(10):
    #     print(next(instructions))

    nodes = get_nodes(data_lines[2:])  # skip first 2 lines
    # print(nodes)

    steps = walk_path(instructions, nodes)
    # print(steps)

    # print(f'End result: {len(steps) - 1}')
    print(f'End result: {steps}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH))
    main(test_data)

    # using test_data using a list to keep track of the steps:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using test_data using an int to keep track of the steps:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

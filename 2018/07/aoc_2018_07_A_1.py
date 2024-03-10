# aoc_2018_07_A_1.py - Day 7: The Sum of Its Parts - part 1
# In what order should the steps in your instructions be completed?
# https://adventofcode.com/2018/day/7


from tools import time_it

from collections import defaultdict

from pprint import pprint


DATA_PATH = './input_2018_07'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_steps(data_lines: list[str]):
    forward_steps = defaultdict(list)
    backward_steps = defaultdict(list)

    for line in data_lines:
        forward_steps[line.split()[1]].append(line.split()[7])
        backward_steps[line.split()[7]].append(line.split()[1])

    return forward_steps, backward_steps


test_data = '''
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    forward_steps, backward_steps = get_steps(data_lines)
    pprint(forward_steps)
    pprint(backward_steps)

    result = ''
    queue = []

    for step in forward_steps:
        if step not in backward_steps:
            queue.append(step)

    while queue:
        queue.sort(reverse=True)  # also works without the reverse and a pop(0)
        step = queue.pop()
        result += step
        for f in forward_steps[step]:
            if all(b in result for b in backward_steps[f]):
                queue.append(f)

    print(f'End result: {result}')


if __name__ == "__main__":
    main(test_data)
    # main(load_data(DATA_PATH))

    # using test_data:
    #   End result: CABDFE
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: HPDTNXYLOCGEQSIMABZKRUWVFJ
    #   Finished 'main' in less than a millisecond

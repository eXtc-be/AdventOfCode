# aoc_2017_25_A_1.py - Day 25: The Halting Problem - part 1
# What is the diagnostic checksum it produces once it's working again?
# https://adventofcode.com/2017/day/25


from tools import time_it

from dataclasses import dataclass, field
from collections import defaultdict

from pprint import pprint


DATA_PATH = './input_2017_25'

DIRECTIONS = {
    'left': -1,
    'right': 1
}


@dataclass
class Instruction:
    condition: int
    action: int
    move: int
    new_state: str


@dataclass
class State:
    name: str
    instructions: list[Instruction] = field(default_factory=list)


@dataclass
class Turing:
    position: int = 0
    slots: defaultdict[int, int] = field(default_factory=lambda: defaultdict(int))
    states: list[State] = field(default_factory=list)

    def do_step(self, state_name: str) -> str:
        state = [s for s in self.states if s.name == state_name][0]
        value = self.slots[self.position]
        instruction = [i for i in state.instructions if i.condition == value][0]
        self.slots[self.position] = instruction.action
        self.position += instruction.move
        return instruction.new_state

    def do_steps(self, start_state, steps: int) -> int:
        current_state = start_state

        for step in range(steps):
            current_state = self.do_step(current_state)

        return self.checksum

    @property
    def checksum(self):
        return sum(self.slots.values())


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_states(data_lines: list[str]) -> list[State]:
    states = []

    instructions = []
    current_state = None
    current_condition = None
    current_action = None
    current_move = None
    new_state = None

    for line in data_lines:
        if line.strip().lower().startswith('in'):
            current_state = line.split()[-1][:-1].lower()  # cut off ':' and convert to lower case
        elif line.strip().lower().startswith('if'):
            current_condition = int(line.split()[-1][:-1])  # cut off ':' and convert to int
        elif line.strip().lower().startswith('- write'):
            current_action = int(line.split()[-1][:-1])  # cut off '.' and convert to int
        elif line.strip().lower().startswith('- move'):
            current_move = DIRECTIONS[line.split()[-1][:-1]]  # cut off '.' and convert to int
        elif line.strip().lower().startswith('- continue'):
            new_state = line.split()[-1][:-1].lower()  # cut off '.' and convert to lower case

        if (
                current_condition is not None and
                current_action is not None and
                current_move is not None and
                new_state is not None
        ):
            instructions.append(Instruction(
                current_condition,
                current_action,
                current_move,
                new_state
            ))
            current_condition = None
            current_action = None
            current_move = None
            new_state = None

        if len(instructions) == 2:
            states.append(State(current_state, instructions))
            instructions = []

    return states


test_data = '''
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    start_state = None
    steps = None

    for line in data_lines:
        if start_state is not None and steps is not None:
            break
        if line.lower().startswith('begin'):
            start_state = line[-2].lower()
        if line.lower().startswith('perform'):
            steps = int(line.split()[-2])

    print(start_state, steps)

    states = get_states(data_lines)
    # pprint(states)

    machine = Turing(states=states)

    result = machine.do_steps(start_state, steps)

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 4225
    #   Finished 'main' in 12 seconds

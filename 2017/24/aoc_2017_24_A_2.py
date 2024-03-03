# aoc_2017_24_A_1.py - Day 24: Electromagnetic Moat - part 1
# What is the strength of the strongest bridge you can make with the components you have available?
# https://adventofcode.com/2017/day/24
# this version runs a bit faster than version 1 by filtering out combinations that don't start with a 0 port
# before they are evaluated


from tools import time_it

from dataclasses import dataclass, field
from itertools import permutations

from pprint import pprint


DATA_PATH = './input_2017_24'

# other constants


@dataclass
class Component:
    ports: list[int] = field(default_factory=list)


@dataclass
class Bridge:
    components: list[Component] = field(default_factory=list)

    def validate(self) -> bool:
        # the first port you use must be of type 0
        if 0 not in self.components[0].ports:
            return False

        # check if every pair of components connects to each other
        used = 0
        for comp_a, comp_b in zip(self.components, self.components[1:]):
            # find the connecting port
            if comp_a.ports[0] == comp_a.ports[1]:  # 2 identical ports, pick any one as the one being used next
                used = comp_a.ports[0]
            else:  # 2 different ports, pick the one that is not previously used as the one being used next
                used = [port for port in comp_a.ports if port != used][0]
            if used not in comp_b.ports:  # verify if the next component has that port type
                return False
            # used = comp_b.ports.remove(used)[0]  #

        return True

    def strength(self):
        return sum([sum(port for port in component.ports) for component in self.components])


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_components(data_lines: list[str]) -> list[Component]:
    return [Component([int(port) for port in line.split('/')]) for line in data_lines]


def _combinations(components: list[Component]) -> list[Component]:
    for i in range(len(components)):
        # yield from permutations(components, i+1)
        for combo in permutations(components, i+1):
            if 0 in combo[0].ports:
                yield combo


test_data = '''
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    components = get_components(data_lines)
    # pprint(components)

    # print(len(list(_combinations(components))))
    valid_bridges = [Bridge(list(combo)) for combo in _combinations(components) if Bridge(list(combo)).validate()]
    # print(len(valid_bridges))

    print(f'End result: {max(bridge.strength() for bridge in valid_bridges)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 31
    #   Finished 'main' in 60 milliseconds
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

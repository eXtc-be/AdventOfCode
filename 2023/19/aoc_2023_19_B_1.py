# aoc_2023_19_B_1.py - Day 19: Aplenty - part 2
# How many distinct combinations of ratings will be accepted by the Elves' workflows?
# https://adventofcode.com/2023/day/19


from aoc_2023_19_A_1 import (
    DATA_PATH,
    load_data,
    ACCEPTED,
    REJECTED,
    Category
)

from tools import time_it

from dataclasses import dataclass, field
from operator import lt, gt
from typing import Callable

from pprint import pprint


MIN_VALUE, MAX_VALUE = 1, 10
START = 'in'


@dataclass
class Condition:
    category: Category
    operator: Callable
    value: int

    def __post_init__(self) -> None:
        if self.operator not in (lt, gt):
            raise ValueError(f'Not a valid operator: {self.operator}')

    @property
    def true_false_values(self) -> tuple[int, int]:
        if self.operator is lt:
            return ((self.value - 1) - MIN_VALUE) + 1, (MAX_VALUE - self.value) + 1
        else:  # gt
            return (MAX_VALUE - (self.value + 1)) + 1, (self.value - MIN_VALUE) + 1


@dataclass
class Rule:
    destination: str
    condition: Condition = None

    @property
    def true_false_values(self) -> tuple[int, int, str]:
        true_value, false_value = 1, 1  # default values - TODO: what should these really be?

        if self.condition:
            true_value, false_value = self.condition.true_false_values

        if self.destination == REJECTED:
            return 0, 0, REJECTED
        elif self.destination == ACCEPTED:
            return true_value, 0, ACCEPTED
        else:
            return 0, 0, self.destination


@dataclass
class Workflow:
    rules: list[Rule] = field(default_factory=list)


def _extract_condition(condition: str) -> Condition:
    """creates a Condition object from the condition string"""
    category, operator, value = None, None, None
    if '<' in condition:
        category, value = condition.split('<')
        operator = lt
    elif '>' in condition:
        category, value = condition.split('>')
        operator = gt

    return Condition(Category(category), operator, int(value))


def _extract_rule(rule: str) -> Rule:
    """takes a string and extracts a Rule object from it, with or without condition"""
    if ':' in rule:
        return Rule(rule.split(':')[1], _extract_condition(rule.split(':')[0]))
    else:
        return Rule(rule)


def _extract_rules(rulez: str) -> list[Rule]:
    """returns a list of rules extracted from the rulez string"""
    return [_extract_rule(rule) for rule in rulez.split(',')]


def _extract_workflow(data_line: str) -> tuple[str, Workflow]:
    """processes one line of data and extracts a Workflow instance from it"""
    name = data_line[:data_line.find('{')]
    rules = _extract_rules(data_line[data_line.find('{') + 1:data_line.find('}')])
    return name, Workflow(rules)


def extract_workflows(data_lines: list[str]) -> dict[str, Workflow]:
    """takes the data_lines and extracts the workflows and parts from them"""
    workflows: dict[str, Workflow] = {}
    for line in data_lines:
        if not line:
            break  # empty line marks the start of the parts section, which we can totally skip for this puzzle
        else:
            name, workflow = _extract_workflow(line)
            workflows[name] = workflow

    return workflows


def get_combinations(workflows: dict[str, Workflow], node: str, rule: Rule, next_rules: list[Rule]) -> int:
    total = 0

    true_value, false_value, next_node = rule.true_false_values
    if next_node == ACCEPTED:
        total += true_value
    elif next_node == REJECTED:
        total += 0
    else:
        total += true_value + false_value * get_combinations(workflows, next_node)

    return total



@time_it
def main(data_lines: list[str]) -> None:
    workflows = extract_workflows(data_lines)
    # pprint(workflows)

    combos = get_combinations(workflows, START)

    print(combos)

    # print(f'End result: {0}')


test_data = '''
in{s>5:A,A}
'''.strip().splitlines()


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

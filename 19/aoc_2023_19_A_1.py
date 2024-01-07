# aoc_2023_19_A_1.py - Day 19: Aplenty - part 1
# Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?
# https://adventofcode.com/2023/day/19


from tools import time_it

from dataclasses import dataclass, field
# from enum import Enum, auto
from operator import lt, gt
from typing import Callable

from pprint import pprint


DATA_PATH = './input_2023_19'

CATEGORIES = list('XMAS')

ACCEPTED = 'A'
REJECTED = 'R'


@dataclass
class Category:
    name: str

    def __post_init__(self):
        self.name = self.name.upper()
        if self.name not in CATEGORIES:
            raise ValueError(f'Not a valid category: {self.name}')


@dataclass
class Condition:
    category: Category
    operator: Callable
    value: int

    def __post_init__(self):
        if self.operator not in (lt, gt):
            raise ValueError(f'Not a valid operator: {self.operator}')

    def process_part(self, part: 'Part') -> bool:
        return self.operator(part[self.category].value, self.value)


@dataclass
class Rule:
    destination: str
    condition: Condition = None

    def process_part(self, part: 'Part') -> bool:
        if self.condition:
            return self.condition.process_part(part)
        else:  # last rule in the list
            return True


@dataclass
class Workflow:
    name: str
    rules: list[Rule] = field(default_factory=list)

    def process_part(self, part: 'Part') -> str:
        for rule in self.rules:
            if rule.process_part(part):
                return rule.destination

        return REJECTED  # this point should never be reached, but just in case..


@dataclass
class Workflows:
    workflows: list[Workflow] = field(default_factory=list)

    def process_part(self, part: 'Part') -> None:
        """sends the part through the workflows and updates its status"""
        next = 'in'
        while next not in [ACCEPTED, REJECTED]:
            current_workflow = self[next]
            next = current_workflow.process_part(part)

        part.status = next

    def __getitem__(self, index):
        """returns the workflow with name == index"""
        if not isinstance(index, str):
            raise ValueError(f'Not a valid index: {index}')

        for workflow in self.workflows:
            if workflow.name == index:
                return workflow

        raise IndexError(f'Not a valid index: {index}')


@dataclass
class Parameter:
    category: Category
    value: int


@dataclass
class Part:
    parameters: list[Parameter] = field(default_factory=list)
    status: str = None

    def __getitem__(self, index):
        if not isinstance(index, Category):
            raise ValueError(f'Not a valid index: {index}')

        return self.parameters[CATEGORIES.index(index.name)]

    @property
    def value(self):
        return sum(param.value for param in self.parameters)

    def __str__(self):
        return (f'{{'
                f'{",".join(f"{param.category.name}={param.value}" for param in self.parameters)}'
                f'}} = {self.value}')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().strip().splitlines()


def _extract_condition(condition: str) -> Condition:
    """creates a Condition object form the condition string"""
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


def extract_workflow(data_line: str) -> Workflow:
    """processes one line of data and extracts a Workflow instance from it"""
    name = data_line[:data_line.find('{')]
    rules = _extract_rules(data_line[data_line.find('{') + 1:data_line.find('}')])
    return Workflow(name, rules)


def _extract_parameter(parameter: str) -> Parameter:
    """extracts one parameter extracted from a string"""
    return Parameter(Category(parameter.split('=')[0]), int(parameter.split('=')[1]))


def _extract_parameters(data_line: str) -> list[Parameter]:
    """returns a list of parameters extracted from data_line"""
    return [_extract_parameter(parameter) for parameter in data_line[1:-1].split(',')]


def extract_part(data_line: str) -> Part:
    """extracts one part from a data line"""
    return Part(_extract_parameters(data_line))


def extract_workflows_and_parts(data_lines: list[str]) -> tuple[Workflows, list[Part]]:
    """takes the data_lines and extracts the workflows and parts from them"""
    workflows = []
    parts = []
    current = 'workflows'
    for line in data_lines:
        if not line:
            current = 'parts'
        elif current == 'workflows':
            workflows.append(extract_workflow(line))
        else:
            parts.append(extract_part(line))

    return Workflows(workflows), parts


def process_parts(parts: list[Part], workflows: Workflows) -> None:
    """takes all parts through the workflows and updates their status member"""
    for part in parts:
        workflows.process_part(part)


test_data = '''
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    workflows, parts = extract_workflows_and_parts(data_lines)
    # pprint(workflows)
    # pprint(parts)

    process_parts(parts, workflows)
    # for part in parts:
    #     if part.status == ACCEPTED:
    #         print(part)

    print(f'End result: {sum(part.value for part in parts if part.status == ACCEPTED)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 19114
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 406934
    #   Finished 'main' in 25 millisecondsa

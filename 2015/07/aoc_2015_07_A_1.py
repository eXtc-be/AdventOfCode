# aoc_2015_07_A_1.py - Day 7: Some Assembly Required - part 1
# In little Bobby's kit's instructions booklet (provided as your puzzle input),
# what signal is ultimately provided to wire a?
# https://adventofcode.com/2015/day/7


from tools import time_it

from operator import and_, or_, lshift, rshift, inv
from dataclasses import dataclass, field
from typing import Callable

from pprint import pprint


DATA_PATH = './input_2015_07'

OPERATORS = {
    'AND': and_,
    'OR': or_,
    'LSHIFT': lshift,
    'RSHIFT': rshift,
    'NOT': inv
}

LITERAL = '='


# global variable cache
cache: dict[str, int] = {}

@dataclass
class Wire:
    arguments: tuple[str | int, str | int | None] = field(default_factory=tuple)
    operation: Callable | str = None
    destination: str = None


@dataclass
class WireList:
    wires: list[Wire] = field(default_factory=list)

    def get_wires(self, instruction_list: list[str]) -> None:
        for instruction_line in instruction_list:
            source, destination = instruction_line.split(' -> ')
            parts = source.split()
            arg_list = None, None
            if len(parts) == 1:
                operation = LITERAL
                arg = parts[0]
                if parts[0].isdigit():
                    arg = int(arg)
                arg_list = arg, None
            elif len(parts) == 2:
                operation = OPERATORS.get(parts[0].upper(), None)
                arg = parts[1]
                if arg.isdigit():
                    arg = int(arg)
                arg_list = arg, None
            elif len(parts) == 3:
                arg1 = parts[0]
                if arg1.isdigit():
                    arg1 = int(arg1)
                operation = OPERATORS.get(parts[1].upper(), None)
                arg2 = parts[2]
                if arg2.isdigit():
                    arg2 = int(arg2)
                arg_list = arg1, arg2
            else:
                raise ValueError(f'Invalid instruction: {instruction_line}')
            self.wires.append(Wire(arg_list, operation, destination))

    def evaluate_wire(self, wire: Wire) -> int:
        if wire.destination in cache:
            return cache[wire.destination]

        if wire.operation == LITERAL:
            if isinstance(wire.arguments[0], int):
                retval = wire.arguments[0]
                # print(f'{wire.destination} = {retval}')
                cache[wire.destination] = retval
                return retval
            else:
                retval = self.evaluate_wire(self[wire.arguments[0]])
                # print(f'{wire.destination} = {retval}')
                cache[wire.destination] = retval
                return retval
        else:
            arg1, arg2 = wire.arguments

            if not isinstance(arg1, int):
                arg1 = self.evaluate_wire(self[arg1])

            if arg2 is None:
                retval = wire.operation(arg1)
                # print(f'{wire.destination} = {retval}')
                cache[wire.destination] = retval
                return retval
            else:
                if not isinstance(arg2, int):
                    arg2 = self.evaluate_wire(self[arg2])

                retval = wire.operation(arg1, arg2)
                # print(f'{wire.destination} = {retval}')
                cache[wire.destination] = retval
                return retval

    def __getitem__(self, item: str) -> Wire:
        if isinstance(item, str):
            for wire in self.wires:
                if wire.destination == item:
                    return wire

        raise IndexError(f'Not a valid index: {item}')

    def __setitem__(self, item: str, value: int) :
        if isinstance(item, str):
            self[item].operation = LITERAL
            self[item].arguments = value, None
        else:
            raise IndexError(f'Not a valid index: {item}')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()



# test_data = '''
# bn RSHIFT 2 -> bo
# lf RSHIFT 1 -> ly
# fo RSHIFT 3 -> fq
# cj OR cp -> cq
# fo OR fz -> ga
# t OR s -> u
# lx -> a
# NOT ax -> ay
# he RSHIFT 2 -> hf
# lf OR lq -> lr
# '''.strip().splitlines()

test_data = '''
5 -> x
6 -> y
x AND y -> d
x OR y -> e
e LSHIFT d -> a
'''.strip().splitlines()

# test_data = '''
# 123 -> x
# 456 -> y
# x AND y -> d
# x OR y -> e
# x LSHIFT 2 -> f
# y RSHIFT 2 -> g
# NOT x -> h
# NOT y -> i
# '''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    wires = WireList()
    wires.get_wires(data_lines)
    # pprint(wires)
    # print(wires['a'])
    # print(wires.evaluate_wire(wires['a']))
    # print(wires.evaluate_wire(wires['e']))
    # print(wires.evaluate_wire(wires['a']))

    print(f'End result: {wires.evaluate_wire(wires["a"])}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 46065
    #   Finished 'main' in 4 milliseconds

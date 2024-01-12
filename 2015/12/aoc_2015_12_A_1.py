# aoc_2015_12_A_1.py - Day 12: JSAbacusFramework.io - part 1
# What is the sum of all numbers in the document?
# https://adventofcode.com/2015/day/12


from tools import time_it

import re

from pprint import pprint

DATA_PATH = './input_2015_12'

NUMBERS = re.compile(r'-?\d+')


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
{"e":86,"c":23,"a":{"a":[120,169,"green","red","orange"],"b":"red"},"g":"yellow","b":["yellow"],"d":"red","f":-19}
{"e":[[{"e":86,"c":23,"a":{"a":[120,169,"green","red","orange"],"b":"red"},"g":"yellow","b":["yellow"],"d":"red","f":-19},{"e":-47,"a":[2],"d":{"a":"violet"},"c":"green","h":"orange","b":{"e":59,"a":"yellow","d":"green","c":47,"h":"red","b":"blue","g":"orange","f":["violet",43,168,78]},"g":"orange","f":[{"e":[82,-41,2,"red","violet","orange","yellow"],"c":"green","a":77,"g":"orange","b":147,"d":49,"f":"blue"},-1,142,136,["green","red",166,-21],"blue","orange",{"a":38}]},"orange","yellow"],"green",-22,[37,[4,-40,["red","yellow",["yellow",177,"red","blue",139,[55,13,"yellow","violet",-21,140,"yellow",117],"blue","blue",106],"blue",{"a":23}],183,92,"orange","green"],"orange"],-5]}
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    numbers = [int(number_string) for number_string in NUMBERS.findall(data_lines[0])]
    result = sum(numbers)

    print(f'End result: {result}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using input data:
    #   End result: 111754
    #   Finished 'main' in 1 millisecond

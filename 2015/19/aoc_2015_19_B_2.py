# aoc_2015_19_B_2.py - Day 19: Medicine for Rudolph - part 2
# Given the available replacements and the medicine molecule in your puzzle input,
# what is the fewest number of steps to go from e to the medicine molecule?
# https://adventofcode.com/2015/day/19

# Possible solution found on reddit:
#   https://old.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4k8ca/


from aoc_2015_19_A_1 import (
    DATA_PATH,
    load_data,
    get_data,
)

from tools import time_it

import re

from pprint import pprint


# other constants


test_data = '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    molecule = data_lines[-1][::-1]
    reps = {m[1][::-1]: m[0][::-1]
            for m in re.findall(r'(\w+) => (\w+)', '\n'.join(data_lines))}

    steps = [molecule]

    def rep(x):
        return reps[x.group()]

    count = 0
    while molecule != 'e':
        molecule = re.sub('|'.join(reps.keys()), rep, molecule, 1)
        steps.append(molecule[::-1])
        count += 1

    print(count)
    print("\n".join(reversed(steps)))


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: this strategy does not work with the example data
    #   Finished 'main' xxx
    # using input data:
    #   End result: 207
    #   Finished 'main' in 4 milliseconds

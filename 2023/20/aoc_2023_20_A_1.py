# aoc_2023_20_A_1.py - Day 20: Pulse Propagation - part 1
# Consult your module configuration;
# determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times,
# waiting for all pulses to be fully handled after each push of the button.
# What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?
# https://adventofcode.com/2023/day/20


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2023_20'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
<testdata>
<testdata>
<testdata>
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # your code

    print(f'End result: {0}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

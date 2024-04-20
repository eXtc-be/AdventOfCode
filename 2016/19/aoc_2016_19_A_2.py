# aoc_2016_19_A_2.py - Day 19: An Elephant Named Joseph - part 1
# With the number of Elves given in your puzzle input, which Elf gets all the presents?
# https://adventofcode.com/2016/day/19
# strategy 2: using the formula from https://www.youtube.com/watch?v=uCsD3ZGzMgE
#   W(n)=2*l+1 for n=2^a+l where l<2^a


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2016_19'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions


test_data = '''
5
'''.strip().splitlines()


@time_it
def main(num_elves: int) -> None:
    b = f'{num_elves:b}'  # convert number of elves to binary
    l = int(b[1:], 2)  # convert the binary string, without the MSB, back to decimal to get l
    w = int(b[1:] + b[0], 2)  # alternatively use the binary trick from the end of the video to get the winner directly

    print(f'End result: {2 * l + 1} - {w}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(int(data_lines[0]))
    # using input data:
    #   End result: 1830117
    #   Finished 'main' in less than a millisecond

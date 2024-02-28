# aoc_2017_19_A_1.py - Day 19: A Series of Tubes - part 1
# What letters will the little packet see (in the order it would see them) if it follows the path?
# https://adventofcode.com/2017/day/19


from tools import time_it

from typing import NamedTuple

from pprint import pprint

DATA_PATH = './input_2017_19'

DIRECTIONS = {
   '|': [(1, 0), (-1, 0)],
   '-': [(0, 1), (0, -1)],
   '+': [(0, 1), (0, -1), (1, 0), (-1, 0)],
}


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_network(data_lines: list[str]) -> list[str]:
    return [line for line in data_lines if line.strip()]


def find_path(network: list[str]) -> tuple[str, int]:
    path = ''
    steps = 0

    # find starting point
    pipe = '|'
    row = 0
    col = network[row].index(pipe)
    current_dir = (1, 0)

    while True:
        # copy associated directions, but leave out the inverse of the current direction (don't go back)
        search_dirs = [d for d in DIRECTIONS[pipe] if d != (-current_dir[0], -current_dir[1])]  # deep copy

        for search_dir in search_dirs:
            if (0 <= row + search_dir[0] < len(network)
                    and 0 <= col + search_dir[1] < len(network[row])):
                new_pipe = network[row + search_dir[0]][col + search_dir[1]]
                if new_pipe != ' ':
                    # update direction, row, column and steps
                    current_dir = search_dir
                    row += search_dir[0]
                    col += search_dir[1]
                    steps += 1

                    # check for letters
                    if new_pipe.isalpha():
                        path += new_pipe
                        new_pipe = [p for p in '|-' if current_dir in DIRECTIONS[p]][0]

                    # keep direction for crossings (- over | or | over -)
                    if new_pipe in '|-' and pipe in '|-':
                        new_pipe = pipe

                    pipe = new_pipe
                    break  # break from for search_dir..
        else:  # no new pipe found - end of the path
            break

    return path, steps + 1


test_data = '''
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
'''.splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    network = get_network(data_lines)
    # print('\n'.join(row.replace(' ', '.') for row in network))

    path, steps = find_path(network)
    # print(path, steps)

    print(f'End result: {path}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: ABCDEF
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: LXWCKGRAOY
    #   Finished 'main' in 15 milliseconds

# aoc_2016_19_A_1.py - Day 19: An Elephant Named Joseph - part 1
# With the number of Elves given in your puzzle input, which Elf gets all the presents?
# https://adventofcode.com/2016/day/19
# strategy 1: looping through all elves stealing presents until 1 elf has them all
#   could be optimized by checking if an elf has all the presents in the inner loop and breaking,
#   instead of looping through all elves at the start of each outer loop to check if any has all the presents


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
    elves = {num: 1 for num in range(num_elves)}
    # print(elves)

    while not any(num == num_elves for num in elves.values()):
        for i in range(num_elves):
            if elves[i]:
                j = i + 1
                while not elves[j % num_elves]:
                    j += 1
                elves[i] += elves[j % num_elves]
                elves[j % num_elves] = 0

    print(f'End result: {[elf for elf, num in elves.items() if num == num_elves][0]+1}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(41)
    # main(int(data_lines[0]))
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1830117
    #   Finished 'main' in 11 seconds

# aoc_2017_12_B_1.py - Day 12: Digital Plumber - part 2
# How many groups are there in total?
# https://adventofcode.com/2017/day/12


from aoc_2017_12_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    ROOT,
    get_programs,
    get_distances,
)

from tools import time_it

from sys import maxsize

from pprint import pprint


# other constants


# other functions


test_data = '''
0 <-> 2
1 <-> 5
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 1
6 <-> 4
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    programs = get_programs(data_lines)
    # print(programs)

    target = ROOT
    groups = [target]

    while True:
        distances = get_distances(programs, target)
        # print(distances)

        # remove programs that are connected to the current target
        #   (overwrite program list with programs that have maxsize distance)
        programs = {id: conn for id, conn in programs.items() if distances[id] == maxsize}
        # print(programs)

        if programs:
            target = list(programs.keys())[0]
            groups.append(target)
        else:
            break

    # print(groups)

    print(f'End result: {len(groups)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 181
    #   Finished 'main' in 9.6 seconds

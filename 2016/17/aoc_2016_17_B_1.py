# aoc_2016_17_B_1.py - Day 17: Two Steps Forward - part 2
# What is the length of the longest path that reaches the vault?
# https://adventofcode.com/2016/day/17


from aoc_2016_17_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    create_rooms,
    find_all_paths,
    find_room
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(start_code: str) -> None:
    rooms = create_rooms()
    # pprint(rooms)

    all_paths = find_all_paths(
        rooms,
        start_code,
        find_room(rooms, 0, 0),
        ''
    )  # find all paths starting with room in upper left corner
    # pprint(all_paths)

    if all_paths:
        print(f'End result: {max(len(path) for path in all_paths)}')
    else:
        print('No solution found')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines[0])
    # using test_data ihgpwlah:
    #   End result: 370
    #   Finished 'main' in 176 milliseconds
    # using test_data kglvqrro:
    #   End result: 492
    #   Finished 'main' in 280 milliseconds
    # using test_data ulqzkmiv:
    #   End result: 830
    #   Finished 'main' in 293 milliseconds
    # using input data:
    #   End result: 500
    #   Finished 'main' in 176 milliseconds

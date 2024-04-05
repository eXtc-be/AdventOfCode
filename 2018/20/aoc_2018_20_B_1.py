# aoc_2018_20_B_1.py - Day 20: A Regular Map - part 2
# How many rooms have a shortest path from your current location that pass through at least 1000 doors?
# https://adventofcode.com/2018/day/20


from aoc_2018_20_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_rooms,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data: str) -> None:
    print(data)

    rooms, distances = get_rooms(data)
    # pprint(rooms)
    # print('\n'.join(''.join(char for char in row) for row in construct_maze(rooms)))

    # pprint(distances)

    print(f'End result: {len([distance for distance in distances.values() if distance >= 1000])}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])

    # using input data:
    #   End result: 8281
    #   Finished 'main' in 11 seconds

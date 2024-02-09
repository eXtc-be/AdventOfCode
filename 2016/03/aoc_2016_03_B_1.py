# aoc_2016_03_B_1.py - Day 3: Squares With Three Sides - part 2
# In your puzzle input, how many of the listed triangles are possible?
# https://adventofcode.com/2016/day/3


from aoc_2016_03_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    validate_triangle
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def get_triangles(datalines: list[str]) -> list[list[int]]:
    triangles = []
    for group in range(len(datalines) // 3):
        temp = [[], [], []]
        for line in range(3):
            values = [int(value) for value in datalines[group * 3 + line].split()]
            for i in range(3):
                temp[i].append(values[i])
        triangles.extend(temp)

    return triangles



@time_it
def main(data_lines: list[str]) -> None:
    triangles = get_triangles(data_lines)
    # pprint(triangles)

    valid_triangles = [triangle for triangle in triangles if validate_triangle(triangle)]
    # pprint(valid_triangles)

    print(f'End result: {len(valid_triangles)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1649
    #   Finished 'main' in 5 milliseconds

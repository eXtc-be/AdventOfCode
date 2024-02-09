# aoc_2016_03_A_1.py - Day 3: Squares With Three Sides - part 1
# In your puzzle input, how many of the listed triangles are possible?
# https://adventofcode.com/2016/day/3


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2016_03'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_triangles(datalines: list[str]) -> list[list[int]]:
    return [[int(v) for v in line.split()] for line in datalines]


def validate_triangle(triangle: list[int]) -> bool:
    for i in range(3):
        copy = triangle[:]  # deep copy
        a = copy.pop(i)
        b, c = copy
        if a >= b + c:
            return False

    return True


test_data = '''
5 10 13
5 10 25
8 15 20
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    triangles = get_triangles(data_lines)
    # pprint(triangles)

    valid_triangles = [triangle for triangle in triangles if validate_triangle(triangle)]
    # pprint(valid_triangles)

    print(f'End result: {len(valid_triangles)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 1
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 917
    #   Finished 'main' in 4 milliseconds

    # test validate_triangle()
    # validate_triangle([1, 2, 3])

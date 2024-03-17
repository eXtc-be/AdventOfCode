# aoc_2018_11_A_1.py - Day 11: Chronal Charge - part 1
# What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?
# https://adventofcode.com/2018/day/11


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2018_11'

GRID_SIZE = 300


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def calc_power_cell(x: int, y: int, serial: int) -> int:
    return int(('00' + str(((x + 10) * y + serial) * (x + 10)))[-3]) - 5


def create_grid(serial: int, grid_size: int = GRID_SIZE) -> list[list[int]]:
    return [[calc_power_cell(x, y, serial) for x in range(1, grid_size + 1)] for y in range(1, grid_size + 1)]


def calc_power_subgrid(grid: list[list[int]], sub_size: int = 3) -> list[tuple[int, int, int]]:
    return [
            (x, y, sum(
                sum(grid[y+dy][x+dx]
                    for dx in range(sub_size)
                    )for dy in range(sub_size)
            ))
            for x in range(len(grid[0])-sub_size) for y in range(len(grid)-sub_size)
    ]


# def calc_power_subgrid(grid: list[list[int]]) -> list[list[int]]:
#     return [
#         [
#             sum(
#                 sum(grid[y+dy][x+dx]
#                     for dx in range(3)
#                     )for dy in range(3)
#             )
#             for x in range(len(grid[y])-3)
#         ]
#         for y in range(len(grid)-3)
#     ]
#
#
@time_it
def main(data: str) -> None:
    serial = int(data)
    # print(serial)
    # print('\n'.join(' '.join(f"{el:2}" for el in line) for line in create_grid(serial)))
    # print('-' * 100)
    # print('\n'.join(' '.join(f"{el:3}" for el in line) for line in calc_power_subgrid(create_grid(serial))))
    # print('-' * 100)
    subgrids = calc_power_subgrid(create_grid(serial))
    largest = max([subgrid for subgrid in subgrids], key=lambda x: x[2])
    print(largest)
    # print('-' * 100)

    print(f'End result: {largest[0]+1},{largest[1]+1}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # for serial in [18, 42]:
    #     main(str(serial))

    # using test_data 18:
    #   End result: 33,45
    #   Finished 'main' in 14 milliseconds
    # using test_data 42:
    #   End result: 21,61
    #   Finished 'main' in 13 milliseconds
    # using input data:
    #   End result: 235,63
    #   Finished 'main' in 329 milliseconds

    # # test calc_power_cell
    # for x, y, serial in [
    #     (3, 5, 8),       # 4
    #     (122, 79, 57),   # -5
    #     (217, 196, 39),  # 0
    #     (101, 153, 71),  # 4
    # ]:
    #     print(f'({x}, {y}), {serial} -> {calc_power_cell(x, y, serial)}')

    # # test create_grid
    # for serial in [18, 42]:
    #     print(serial)
    #     print('\n'.join(' '.join(f"{el:2}" for el in line) for line in create_grid(serial, 64)))
    #     print('-' * 100)

    # # test calc_power_subgrid
    # for serial in [18, 42]:
    #     print(serial)
    #     print('\n'.join(' '.join(f"{el:2}" for el in line) for line in create_grid(serial, 65)))
    #     print('-' * 100)
    #     print('\n'.join(' '.join(f"{el:3}" for el in line) for line in calc_power_subgrid(create_grid(serial, 65))))
    #     print('-' * 100)
    #     subgrids = calc_power_subgrid(create_grid(serial, 65))
    #     largest = max([subgrid for subgrid in subgrids], key=lambda x: x[2])
    #     print(largest)
    #     print('-' * 100)

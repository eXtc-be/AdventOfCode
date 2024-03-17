# aoc_2018_11_B_1.py - Day 11: Chronal Charge - part 2
# What is the X,Y,size identifier of the square with the largest total power?
# https://adventofcode.com/2018/day/11


from aoc_2018_11_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
    create_grid,
    calc_power_subgrid,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data: str) -> None:
    serial = int(data)
    # print(serial)

    absolute_largest = None

    for sub_size in range(1, 301):
        subgrids = calc_power_subgrid(create_grid(serial), sub_size=sub_size)
        largest = max([subgrid for subgrid in subgrids], key=lambda x: x[2])
        print(sub_size, largest)
        # https://old.reddit.com/r/adventofcode/comments/lh1qa2/2018_day_11_part_2_python_code_optimization/gmuvq5n/
        if largest[2] < 0:
            break
        if absolute_largest is None or largest[2] > absolute_largest[0][2]:
            absolute_largest = largest, sub_size

    print(absolute_largest)

    print(f'End result: {absolute_largest[0][0]+1},{absolute_largest[0][1]+1},{absolute_largest[1]}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # for serial in [18, 42]:
    #     main(str(serial))

    # main(data_lines)
    # using test_data 18:
    #   End result: 90,269,16
    #   Finished 'main' in 1 minute and 58 seconds
    # using test_data 42:
    #   End result: 232,251,12
    #   Finished 'main' in 1 minute and 10 seconds
    # using input data:
    #   End result: 229,251,16
    #   Finished 'main' in 49 seconds

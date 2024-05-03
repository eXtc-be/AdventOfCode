# aoc_2019_15_B_1.py - Day 15: Oxygen System - part 2
# How many minutes will it take to fill the grid with oxygen?
# https://adventofcode.com/2019/day/15


from aoc_2019_15_A_1 import (
    DATA_PATH,
    MAZE_PATH,
    Grid,
    Robot,
    Computer,
    load_data,
    map_grid,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


test_data = '''
 ##   
#..## 
#.#..#
#.O.# 
 ###  
'''.strip().splitlines()


@time_it
def main(data: str, verbose: bool = False, confirm: bool = False) -> None:
    grid = Grid()
    # robot = Robot(Computer(list(map(int, data.split(','))), [], False))

    # map_grid(grid, robot, verbose, confirm)
    # grid.draw()
    # print(f'origin: {grid.origin} - oxygen: {grid.oxygen}')

    grid.load(load_data(MAZE_PATH))
    # grid.draw()
    # print(f'origin: {grid.origin} - oxygen: {grid.oxygen}')

    distances = grid.find_distances()
    # pprint(distances)

    print(f'End result: {max(distances.values())}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])

    # using input data:
    #   End result: 398
    #   Finished 'main' in 1 second (without mapping the grid)

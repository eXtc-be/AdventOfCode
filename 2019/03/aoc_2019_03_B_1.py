# aoc_2019_03_B_1.py - Day 3: Crossed Wires - part 2
# What is the fewest combined steps the wires must take to reach an intersection?
# https://adventofcode.com/2019/day/3


from aoc_2019_03_A_1 import (
    DATA_PATH,
    DIRECTIONS,
    Point,
    load_data,
    get_wires,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


GRID = {
    0: ' ',
    1: '#',
    2: '*',
    3: 'X',
}


def print_grid(grid: list[list[int]]) -> None:
    print('\n'.join([''.join([GRID[c] for c in row]) for row in grid]))


@time_it
def main(data_lines: list[str]) -> None:
    wires = get_wires(data_lines)

    # calculate the minimum and maximum horizontal and vertical coordinates
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for wire in wires:
        current = Point(0, 0)
        for instruction in wire:
            current += DIRECTIONS[instruction[0]] * int(instruction[1:])
            if current.x < min_x:
                min_x = current.x
            if current.x > max_x:
                max_x = current.x
            if current.y < min_y:
                min_y = current.y
            if current.y > max_y:
                max_y = current.y

    # pre populate grid
    grid = [[0 for _ in range(min_x, max_x+1)] for _ in range(min_y, max_y+1)]

    # mark both wires onto the grid
    for w, wire in enumerate(wires, 1):
        current = Point(-min_x, -min_y)

        for instruction in wire:
            dir, num = DIRECTIONS[instruction[0]], int(instruction[1:])
            for step in range(num):
                current += dir
                if grid[current.y][current.x] == 0:  # not yet visited
                    grid[current.y][current.x] = w
                elif grid[current.y][current.x] == w:  # visited by same wire
                    continue
                elif grid[current.y][current.x] == 3:  # already crossed
                    continue
                else:  # visited by other wire, but not by current wire
                    grid[current.y][current.x] = 3
    # print_grid(grid)

    # find all crossings (3) and remember their coordinates
    crossings = [
        Point(x, y)
        for y in range(len(grid)) for x in range(len(grid[0]))
        if grid[y][x] == 3
    ]
    # print(crossings)

    crossing_steps = {crossing: 0 for crossing in crossings}

    # follow both wires (step by step) and verify update steps if any crossing is met
    for wire in wires:
        current = Point(-min_x, -min_y)
        steps = 0

        for instruction in wire:
            dir, num = DIRECTIONS[instruction[0]], int(instruction[1:])
            for step in range(num):
                current += dir
                steps += 1
                if current in crossing_steps:
                    crossing_steps[current] += steps
    # pprint(crossing_steps)

    print(f'End result: {min(crossing_steps.values())}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0:2])
    # main(test_data[2:4])
    # main(test_data[4:6])

    # using test_data 1:
    #   End result: 30
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 610
    #   Finished 'main' in 4 milliseconds
    # using test_data 3:
    #   End result: 410
    #   Finished 'main' in 2 milliseconds
    # using input data:
    #   End result: 163676
    #   Finished 'main' in 23 seconds

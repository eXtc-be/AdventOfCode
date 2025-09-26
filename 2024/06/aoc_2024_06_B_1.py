# aoc_2024_06_B_1.py - Day 6: Guard Gallivant - part 2
# You need to get the guard stuck in a loop by adding a single new obstruction.
# How many different positions could you choose for this obstruction?
# https://adventofcode.com/2024/day/6


from aoc_2024_06_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    find_guard,
    patrol,
    Coord,
    TURNING,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions

def try_grid(grid: list[list[str]]) -> bool:
    position, heading = find_guard(grid)

    visited = set()
    while True:
        if (position, heading) in visited:
            return True  # loop detected
        else:
            visited.add((position, heading))  # mark visited

            next_pos = position + heading.value
            if 0 <= next_pos.x < len(grid[0]) and 0 <= next_pos.y < len(grid):
                if grid[next_pos.y][next_pos.x] in '^.':
                    position = next_pos
                elif grid[next_pos.y][next_pos.x] in 'O#':
                    heading = TURNING[heading]
                    # position = position + heading.value
                else:
                    raise ValueError(f'unexpected value at {next_pos}: {grid[next_pos.y][next_pos.x]}')
            else:
                return False


@time_it
def main(data_lines: list[str]) -> None:
    grid = [[char for char in line] for line in data_lines]

    position, heading = find_guard(grid)

    # print('\n'.join(''.join(char for char in line) for line in grid))
    # print('-' * 80)

    patrol_grid = patrol(grid)

    # print('\n'.join(''.join(char for char in line) for line in patrol_grid))
    # print('-' * 80)

    candidates = []
    for y, line in enumerate(patrol_grid):
        for x, char in enumerate(line):
            if char == 'X' and Coord(x, y) != position:
                candidates.append(Coord(x, y))

    # print(candidates)
    # print('-' * 80)

    # for candidate in candidates:
        # print('\n'.join(''.join(char for char in line) for line in candidate_grid))
        # print('-' * 80)

    result = sum(
        1 if try_grid(
            [['O' if Coord(x, y) == candidate else char for x, char in enumerate(line)] for y, line in enumerate(grid)]
        )
        else 0
        for candidate in candidates
    )


    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 6
    #   Finished 'main' in 6 milliseconds
    # using input data:
    #   End result: 1480
    #   Finished 'main' in 1 minute and 1 seconds

# aoc_2017_22_B_1.py - Day 22: Sporifica Virus - part 2
# After 10_000_000 bursts of activity, how many bursts cause a node to become infected?
# https://adventofcode.com/2017/day/22
# using the new and improved data structure from aoc_2017_22_A_2 should speed things up


from aoc_2017_22_A_2 import (
    DATA_PATH,
    DIRECTIONS,
    STATES,
    STATES_INV,
    INFECTED,
    WEAKENED,
    FLAGGED,
    CLEAN,
    Point,
    load_data,
    test_data,
    get_grid,
    draw_grid,
)

from tools import time_it

# other imports

from pprint import pprint


HEADINGS = {
    'N': {'L': 'W', 'R': 'E', 'N': 'N', 'T': 'S'},
    'E': {'L': 'N', 'R': 'S', 'N': 'E', 'T': 'W'},
    'S': {'L': 'E', 'R': 'W', 'N': 'S', 'T': 'N'},
    'W': {'L': 'S', 'R': 'N', 'N': 'W', 'T': 'E'},
}

ROUNDS = 10_000_000
ROUNDS_TEST = 10_000


new_infections = 0


def do_step(grid: dict[Point, int], location: Point, heading: str) -> tuple[Point, str]:
    global new_infections
    turn = None

    if STATES_INV[grid[location]] == CLEAN:
        turn = 'L'
        grid[location] = STATES[WEAKENED]
    elif STATES_INV[grid[location]] == WEAKENED:
        turn = 'N'
        grid[location] = STATES[INFECTED]
        new_infections += 1
    elif STATES_INV[grid[location]] == INFECTED:
        turn = 'R'
        grid[location] = STATES[FLAGGED]
    elif STATES_INV[grid[location]] == FLAGGED:
        turn = 'T'
        grid[location] = STATES[CLEAN]

    new_heading = HEADINGS[heading][turn]
    new_location = location + DIRECTIONS[new_heading]

    return new_location, new_heading


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS, verbose: bool = False) -> None:
    global new_infections

    grid = get_grid(data_lines)
    # print(grid)

    min_x = min(p.x for p in grid.keys())
    min_y = min(p.y for p in grid.keys())
    max_x = max(p.x for p in grid.keys())
    max_y = max(p.y for p in grid.keys())

    location = Point(min_x + (max_x - min_x) // 2, min_y + (max_y - min_y) // 2)
    heading = 'N'

    if verbose:
        print(0, location, heading)
        draw_grid(grid, location)
        print('-' * 100)

    for round in range(1, rounds + 1):
        location, heading = do_step(grid, location, heading)
        if verbose:
            print(round, location, heading)
            draw_grid(grid, location)
            print('-' * 100)

    print(f'End result: {new_infections}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, ROUNDS_TEST, False)
    # main(data_lines, 100, False)
    # using test_data with 100 rounds:
    #   End result: 26
    #   Finished 'main' in less than a millisecond
    # using test_data with 10000 rounds:
    #   End result: 2608
    #   Finished 'main' in 17 milliseconds
    # using test_data with 10000000 rounds:
    #   End result: 2511944
    #   Finished 'main' in 17 seconds
    # using input data:
    #   End result: 2512261
    #   Finished 'main' in 17 seconds

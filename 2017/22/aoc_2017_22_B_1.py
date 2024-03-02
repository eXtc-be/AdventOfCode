# aoc_2017_22_B_1.py - Day 22: Sporifica Virus - part 2
# After 10_000_000 bursts of activity, how many bursts cause a node to become infected?
# https://adventofcode.com/2017/day/22


from aoc_2017_22_A_1 import (
    DATA_PATH,
    DIRECTIONS,
    Point,
    load_data,
    test_data,
    get_infected,
    draw_grid,
)

from tools import time_it

# other imports

from pprint import pprint


HEADINGS = {
    'N': {'L': 'W', 'R': 'E', 'N': 'N', 'T': 'S', 'friendly': 'north'},
    'E': {'L': 'N', 'R': 'S', 'N': 'E', 'T': 'W', 'friendly': 'east'},
    'S': {'L': 'E', 'R': 'W', 'N': 'S', 'T': 'N', 'friendly': 'south'},
    'W': {'L': 'S', 'R': 'N', 'N': 'W', 'T': 'E', 'friendly': 'west'},
}

ROUNDS = 10_000_000
ROUNDS_TEST = 100


new_infections = 0


def do_step(
        infected: list[Point],
        weakened: list[Point],
        flagged: list[Point],
        location: Point,
        heading: str
) -> tuple[Point, str]:
    global new_infections
    turn = None

    if location in infected:
        turn = 'R'
        infected.remove(location)
        flagged.append(location)
    elif location in weakened:
        turn = 'N'
        weakened.remove(location)
        infected.append(location)
        new_infections += 1
    elif location in flagged:
        turn = 'T'
        flagged.remove(location)
    else:  # clean
        turn = 'L'
        weakened.append(location)

    new_heading = HEADINGS[heading][turn]
    new_location = location + DIRECTIONS[new_heading]

    return new_location, new_heading


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    global new_infections

    infected = get_infected(data_lines)
    # print(infected)

    weakened = []
    flagged = []

    location = Point(0, 0)
    heading = 'N'

    # print(location, heading, infected)
    # draw_grid(infected, location, Point(-5, -5), Point(5, 5))
    # print('-' * 100)

    for round in range(rounds):
        if round % 1000 == 0:
            print(round, len(infected), len(weakened), len(flagged))

        location, heading = do_step(infected, weakened, flagged, location, heading)
        # print(location, heading, infected)
        # draw_grid(infected, location, Point(-5, -5), Point(5, 5), weakened, flagged)
        # print('-' * 100)

    print(f'End result: {new_infections}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, ROUNDS_TEST)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

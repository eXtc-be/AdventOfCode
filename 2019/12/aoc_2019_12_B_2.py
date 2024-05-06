# aoc_2019_12_B_2.py - Day 12: The N-Body Problem - part 2
# How many steps does it take to reach the first state that exactly matches a previous state?
# https://adventofcode.com/2019/day/12
# knowing that the repeating state is the initial state, we no longer need to keep a list
# (it's actually a set) of all previous states; we just need to count the number of steps until we see
# the initial state again


from aoc_2019_12_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_moons,
)

from tools import time_it

from itertools import combinations
from math import lcm

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    x_cycle = 0
    y_cycle = 0
    z_cycle = 0

    initial_state = get_moons(data_lines)
    moons = get_moons(data_lines)

    # find repeating x-values
    while True:
        # update x-velocities
        for first, second in combinations(moons, 2):
            if first.position.x > second.position.x:
                first.velocity.x -= 1
                second.velocity.x += 1
            elif first.position.x < second.position.x:
                first.velocity.x += 1
                second.velocity.x -= 1
            else:  # first.x == second.x
                pass
        # apply x-velocities
        for moon in moons:
            moon.position.x += moon.velocity.x
        # check if we already saw this state
        if moons == initial_state:
            break
        else:
            x_cycle += 1
    print(f'Found repeating values for x after {x_cycle + 1} steps')

    # find repeating y-values
    while True:
        # update y-velocities
        for first, second in combinations(moons, 2):
            if first.position.y > second.position.y:
                first.velocity.y -= 1
                second.velocity.y += 1
            elif first.position.y < second.position.y:
                first.velocity.y += 1
                second.velocity.y -= 1
            else:  # first.y == second.y
                pass
        # apply y-velocities
        for moon in moons:
            moon.position.y += moon.velocity.y
        # check if we already saw this state
        if moons == initial_state:
            break
        else:
            y_cycle += 1
    print(f'Found repeating values for y after {y_cycle + 1} steps')

    # find repeating z-values
    while True:
        # update z-velocities
        for first, second in combinations(moons, 2):
            if first.position.z > second.position.z:
                first.velocity.z -= 1
                second.velocity.z += 1
            elif first.position.z < second.position.z:
                first.velocity.z += 1
                second.velocity.z -= 1
            else:  # first.z == second.z
                pass
        # apply z-velocities
        for moon in moons:
            moon.position.z += moon.velocity.z
        # check if we already saw this state
        if moons == initial_state:
            break
        else:
            z_cycle += 1
    print(f'Found repeating values for z after {z_cycle + 1} steps')

    print(f'End result: {lcm(x_cycle + 1, y_cycle + 1, z_cycle + 1)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])

    # using test_data 0:
    #   End result: 2772
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 4686774924
    #   Finished 'main' in 39 milliseconds
    # using input data:
    #   End result: 376203951569712
    #   Finished 'main' in 1.42 seconds

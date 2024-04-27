# aoc_2019_11_B_1.py - Day 11: Space Police - part 2
# After starting the robot on a single white panel instead, what registration identifier does it paint on your hull?
# https://adventofcode.com/2019/day/11


from aoc_2019_11_A_1 import (
    DATA_PATH,
    COLOR,
    TURN,
    Robot,
    Computer,
    Hull,
    Color,
    State,
    load_data,
)

from tools import time_it, clear

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data: str, verbose: bool = False, confirm: bool = False) -> None:
    robot = Robot(Computer(list(map(int, data.split(','))), [], verbose))

    hull = Hull(Color.white)
    if verbose:
        clear()
        hull.draw(robot)
        if confirm:
            input()

    while robot.computer.state != State.halted:
        robot.computer.run([hull[robot.position].value])
        hull[robot.position] = COLOR[robot.computer.outputs.pop(0)]
        robot.move(TURN[robot.computer.outputs.pop(0)])
        _ = hull[robot.position]  # access new position to force auto expanding the hull's panels array
        if verbose:
            clear()
            hull.draw(robot)
            print('-' * 100)
            if confirm:
                input()

    hull.draw()


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0], True)

    # using input data:
    #   End result: RKURGKGK
    #   Finished 'main' in 50 milliseconds

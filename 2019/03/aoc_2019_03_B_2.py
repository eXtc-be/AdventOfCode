# aoc_2019_03_B_2.py - Day 3: Crossed Wires - part 2
# What is the fewest combined steps the wires must take to reach an intersection?
# https://adventofcode.com/2019/day/3
# using aoc_2019_03_A_2's optimized functions, this version is much faster and memory efficient


from aoc_2019_03_A_2 import (
    DATA_PATH,
    DIRECTIONS,
    Point,
    load_data,
    get_instructions,
    get_corners,
    find_crossings,
    test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def find_steps(wire: list[Point], point: Point) -> int:
    steps = 0

    for first, last in zip(wire, wire[1:]):  # loop through all segments
        x1, x2 = sorted((first.x, last.x))
        y1, y2 = sorted((first.y, last.y))

        if x1 <= point.x <= x2 and y1 <= point.y <= y2:  # point is in this segment
            steps += abs(first.x - point.x) + abs(first.y - point.y)  # add part of current segments length
            break
        else:  # point is not in this segment
            steps += x2 - x1 + y2 - y1  # add current segments length to steps

    return steps


@time_it
def main(data_lines: list[str]) -> None:
    wires = get_instructions(data_lines)
    # pprint(wires)

    wire_1 = get_corners(wires[0])
    # pprint(wire_1)

    wire_2 = get_corners(wires[1])
    # pprint(wire_2)

    crossings = find_crossings(wire_1, wire_2)
    # pprint(crossings)

    # print(crossings[0], find_steps(wire_1, crossings[0]))
    # print(crossings[0], find_steps(wire_2, crossings[0]))
    # print(crossings[1], find_steps(wire_1, crossings[1]))
    # print(crossings[1], find_steps(wire_2, crossings[1]))

    crossing_steps = {crossing: find_steps(wire_1, crossing) + find_steps(wire_2, crossing) for crossing in crossings}

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
    #   Finished 'main' in less than a millisecond
    # using test_data 3:
    #   End result: 410
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 163676
    #   Finished 'main' in 8 milliseconds

# aoc_2019_17_B_2a.py - Day 17: Set and Forget - part 2
# After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?
# https://adventofcode.com/2019/day/17
# this program takes a scaffolding path and returns the (full) instruction sequence to walk the path
# I'm assuming the robot always goes straight at intersections and only turns at corners


from aoc_2019_17_A_1 import (
    # DATA_PATH,
    SCAFFOLD,
    HEADINGS,
    Coord,
    load_data,
    # test_data,
)

from tools import time_it

# other imports

from pprint import pprint


MAP_PATH = './map.txt'

ROBOT = '^v<>'

# maps old and new direction to a turn (L - left, R - right, S - straight, B - back)
TURNS = {
    Coord(0, -1): {Coord(0, -1): 'S', Coord(0, 1): 'B', Coord(-1, 0): 'L', Coord(1, 0): 'R', },  # up
    Coord(0, 1): {Coord(0, -1): 'B', Coord(0, 1): 'S', Coord(-1, 0): 'R', Coord(1, 0): 'L', },  # down
    Coord(-1, 0): {Coord(0, -1): 'R', Coord(0, 1): 'L', Coord(-1, 0): 'S', Coord(1, 0): 'B', },  # left
    Coord(1, 0): {Coord(0, -1): 'L', Coord(0, 1): 'R', Coord(-1, 0): 'B', Coord(1, 0): 'S', },  # right
}


def trace_path(data_lines: list[str]) -> str:
    instructions = ''

    # find the location of the robot and its current heading
    robot = None
    cur_head = None
    for r, row in enumerate(data_lines):
        found = False
        for c, char in enumerate(row):
            if char in ROBOT:
                robot = Coord(c, r)
                # characters in ROBOT are in the same order as the directions in DIRECTION
                cur_head = HEADINGS[ROBOT.index(char)]
                found = True
                break
        if found:
            break

    # walk the path
    while True:

        # find new heading
        for heading in HEADINGS:
            if 0 <= (robot + heading).x < len(data_lines[0]) and 0 <= (robot + heading).y < len(data_lines):
                if data_lines[(robot + heading).y][(robot + heading).x] == SCAFFOLD:
                    turn = TURNS[cur_head][heading]
                    if turn in 'LR':
                        instructions += turn + ','
                        cur_head = heading
                        break
        else:  # no more turns
            break

        # walk straight for as long as possible
        steps = 0
        while True:
            if 0 <= (robot + cur_head).x < len(data_lines[0]) and 0 <= (robot + cur_head).y < len(data_lines):
                if data_lines[(robot + cur_head).y][(robot + cur_head).x] == SCAFFOLD:
                    robot += cur_head
                    steps += 1
                else:
                    break
            else:
                break

        instructions += str(steps) + ','

    return instructions[:-1]  # remove last comma


test_data = '''
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    print(f'End result: {trace_path(data_lines)}')


if __name__ == "__main__":
    main(load_data(MAP_PATH))  # we could also get the map from aoc_2019_17_B_1, but this is (much) faster
    # main(test_data)

    # using test_data:
    #   End result: R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: L,6,R,12,L,6,L,8,L,8,L,6,R,12,L,6,L,8,L,8,L,6,R,12,R,8,L,8,L,4,L,4,L,6,L,6,R,12,R,8,L,8,L,6,R,12,L,6,L,8,L,8,L,4,L,4,L,6,L,6,R,12,R,8,L,8,L,4,L,4,L,6,L,6,R,12,L,6,L,8,L,8
    #   Finished 'main' in 1 millisecond

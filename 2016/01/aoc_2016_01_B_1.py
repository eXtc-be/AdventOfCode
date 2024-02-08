# aoc_2016_01_B_1.py - Day 1: No Time for a Taxicab - part 2
# How many blocks away is Easter Bunny HQ?
# https://adventofcode.com/2016/day/1


from aoc_2016_01_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_directions,
    HEADINGS,
    TURNS,
    DIRECTIONS
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def check_visited(visited: list[list[int]], current: list[int], previous: list[int]) -> list[int] | None:
    """returns the coordinates of the block previously visited, else None"""
    if current in visited:  # check if current is in visited end points
        return current
    else:
        for first, last in zip(visited, visited[1:]):  # create first, last coordinates from visited list
            if first[0] == last[0]:  # X-coordinates are identical -> vertical line
                if current[0] == previous[0]:  # also a vertical line, so no crossing
                    return None
                else:
                    y1, y2 = sorted((first[1], last[1]))
                    if y1 <= current[1] <= y2:
                        return [first[0], current[1]]
            else:  # using Taxicab geometry, the line must be horizontal if it is not vertical
                if current[1] == previous[1]:  # also a horizontal line, so no crossing
                    return None
                else:
                    x1, x2 = sorted((first[0], last[0]))
                    if x1 <= current[0] <= x2:
                        return [current[0], first[1]]
    return None  # no crossing found


@time_it
def main(direction_string: str) -> None:
    directions = get_directions(direction_string)
    # pprint(directions)

    current_heading = 'N'
    current_position = [0, 0]
    visited = [current_position]
    previously_visited = None

    for direction in directions:
        turn, blocks = direction[0], int(direction[1:])
        current_heading = HEADINGS[current_heading][turn]
        print(f'turning {TURNS[turn]} heading {HEADINGS[current_heading]["friendly"]} moving {blocks} blocks ', end='')
        new_position = [None, None]
        new_position[0] = current_position[0] + DIRECTIONS[current_heading][0] * blocks
        new_position[1] = current_position[1] + DIRECTIONS[current_heading][1] * blocks
        print(f'to position {new_position}')
        visited.append(new_position)
        if len(visited) > 3 and (previously_visited := check_visited(visited, new_position, current_position)):
            break
        current_position = new_position

    print(f'\nFinal position: {previously_visited}')

    print(f'\nDistance from start: {sum(abs(axis) for axis in previously_visited)}')


if __name__ == "__main__":
    # data_lines = load_data(DATA_PATH)
    data_line = 'R8, R4, R4, R8'
    # print(data_line)

    main(data_line)
    # using test_data:
    #   End result: xxx
    #   Finished 'main' in xxx
    # using input data:
    #   End result: xxx
    #   Finished 'main' in xxx

    # test check visited
    # visited = [[0, 0], [8, 0], [8, -4], [4, -4], ]
    # print(check_visited(visited, [4, 4], visited[-1]))

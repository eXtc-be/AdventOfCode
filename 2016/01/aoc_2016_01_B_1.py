# aoc_2016_01_B_1.py - Day 1: No Time for a Taxicab - part 2
# How many blocks away is the first location you visit twice?
# https://adventofcode.com/2016/day/1


from aoc_2016_01_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    Coordinates,
    get_directions,
    HEADINGS,
    TURNS,
    DIRECTIONS
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def check_visited(visited: list[Coordinates], current: Coordinates, previous: Coordinates) -> Coordinates | None:
    """returns the coordinates of the block previously visited, else None"""
    if current in visited:  # check if current is in visited end points
        return current
    else:
        for first, last in zip(visited[:-1], visited[1:-1]):  # create first, last coordinates from visited list
            if first.x == last.x:  # X-coordinates are identical -> vertical line
                if current.x == previous.x:  # also a vertical line, so no crossing
                    continue  # next pair of coordinates
                else:
                    y1, y2 = sorted((first.y, last.y))
                    if y1 <= current.y <= y2:
                        x1, x2 = sorted((current.x, previous.x))
                        if x1 <= first.x <= x2:
                            return Coordinates(first.x, current.y)
            else:  # using Taxicab geometry, the line must be horizontal if it is not vertical
                if current.y == previous.y:  # also a horizontal line, so no crossing
                    continue  # next pair of coordinates
                else:
                    x1, x2 = sorted((first.x, last.x))
                    if x1 <= current.x <= x2:
                        y1, y2 = sorted((current.y, previous.y))
                        if y1 <= first.y <= y2:
                            return Coordinates(current.x, first.y)

    return None  # no crossing found


@time_it
def main(direction_string: str) -> None:
    directions = get_directions(direction_string)
    # pprint(directions)

    current_heading = 'N'
    current_position = Coordinates(0, 0)
    visited = []
    previously_visited = None

    for direction in directions:
        print(f'{direction:4} - ', end='')
        visited.append(Coordinates(current_position.x, current_position.y))  # deep copy
        turn, blocks = direction[0], int(direction[1:])
        current_heading = HEADINGS[current_heading][turn]
        print(f'turning {TURNS[turn]} heading {HEADINGS[current_heading]["friendly"]} moving {blocks} block(s) ', end='')
        current_position.x += DIRECTIONS[current_heading].x * blocks
        current_position.y += DIRECTIONS[current_heading].y * blocks
        print(f'to position {current_position}')
        if len(visited) > 3 and (previously_visited := check_visited(visited, current_position, visited[-1])):
            print(f'=== intersection found at {previously_visited} ===')
            break

    print(f'\nEaster Bunny Headquarters position: {previously_visited}')

    print(f'Distance from start: {previously_visited.distance()}\n')


if __name__ == "__main__":
    data_line = load_data(DATA_PATH)[0]
    # data_line = 'R8, R4, R4, R8'
    # print(data_line)

    main(data_line)
    # using test_data:
    #   End result: 4
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 131
    #   Finished 'main' in 2 milliseconds

    # # test check visited
    # visited = [[0, 0], [8, 0], [8, -4], [4, -4], ]
    # print(check_visited(visited, [4, 4], visited[-1]))  # [4, 0]
    #
    # visited = [[0, 0], [8, 0], [8, 4], [12, 4], ]
    # print(check_visited(visited, [12, -4], visited[-1]))  # None
    #
    # visited = [[0, 0], [4, 0], [4, -4], [5, -4], [5, -7], [10, -7], [10, -9], [5, -9], [5, -8], [1, -8], ]
    # print(check_visited(visited, [1, -5], visited[-1]))  # None
    #
    # visited = [[0, 0], [4, 0], [4, -4], [5, -4], [5, -7], [10, -7], [10, -9], [5, -9], [5, -8], [1, -8], ]
    # print(check_visited(visited, [1, 5], visited[-1]))  # [1, 0]
    #
    # visited = [[0, 0], [4, 0], [4, -4], [5, -4], [5, -7], [10, -7], [10, -9], [5, -9], [5, -8], [1, -8], [1, -5], ]
    # print(check_visited(visited, [4, -5], visited[-1]))  # None
    #
    # visited = [[0, 0], [4, 0], [4, -4], [5, -4], [5, -7], [10, -7], [10, -9], [5, -9], [5, -8], [1, -8], [1, -5], ]
    # print(check_visited(visited, [10, -5], visited[-1]))  # [5, -5]

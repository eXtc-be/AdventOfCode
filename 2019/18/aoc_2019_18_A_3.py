# aoc_2019_18_A_3.py - Day 18: Many-Worlds Interpretation - part 1
# How many steps is the shortest path that collects all the keys?
# https://adventofcode.com/2019/day/18

# inspired by GitHub user https://github.com/mebeim (see extern_1.py)
# https://github.com/mebeim/aoc/blob/master/2019/README.md#day-18---many-worlds-interpretation

# I added caching to get_neighbours and _update_keys. this shaved a couple % off of the runtime, but not much
# I then turned the main searching loop into a recursive function, so it could be cached
#   this helped dramatically: example 4 went from 3 and a half minutes to 471 milliseconds and
#   the actual puzzle went from 24 minutes to 6 seconds (most of that time was spent precalculating paths)
# I could further optimize find_distance, but I feel this is good enough for now
# I also changed the p_distances dict to use str instead of Point as keys,
#   but I don't think that contributed much to any speed gains


from aoc_2019_18_A_1 import (
    DATA_PATH, START, WALL, EMPTY, KEYS, DOORS,
    Node,
    load_data,
    # _update_keys,
    test_data,
)

from aoc_2019_18_A_2 import (
    find_distance,
    Point,
)

from tools import time_it

from itertools import combinations
from sys import maxsize
from functools import lru_cache

from pprint import pprint


# other constants


@lru_cache(27)
def _update_keys(keys: str, new: str) -> str:
    # print(keys, new)
    return ''.join(sorted(set(list(keys) + [new])))


def collect_keys(grid: list[str]) -> int | None:
    all_keys = ''
    points = []

    # find all points of interest (start, keys, doors)
    for r, row in enumerate(grid[1:-1], 1):
        for c, char in enumerate(row[1:-1], 1):
            if char == START or char in KEYS:
                points.append(Point(r, c))
                all_keys = _update_keys(all_keys, char)

    # find the shortest path between all points of interest
    print('precalculating paths')
    p_distances: dict[str, dict[str, tuple[int, set[str]]]] = {grid[p.row][p.col]: {} for p in points}
    for combo in combinations(points, 2):
        # print(f'{combo[0]} <-> {combo[1]}', end=': ')
        distance, doors = find_distance(grid, *combo)
        # print(distance, doors)
        p_distances[grid[combo[0].row][combo[0].col]][grid[combo[1].row][combo[1].col]] = distance, doors
        p_distances[grid[combo[1].row][combo[1].col]][grid[combo[0].row][combo[0].col]] = distance, doors

    @lru_cache(2 ** len(all_keys))
    def get_neighbors(node: str, keys: str) -> list[tuple[str, int]]:
        neighbors = []

        for neighbor, (distance, doors) in p_distances[node].items():
            if neighbor not in keys and neighbor in all_keys and all(door.lower() in keys + node for door in doors):
                neighbors.append((neighbor, distance))

        return neighbors

    # use precalculated paths to find all keys
    print('collecting keys')
    counter = 0

    @lru_cache(2 ** len(all_keys))
    def find_keys(src: str, keys: str) -> int:
        if _update_keys(keys, src) == all_keys:
            return 0

        best = maxsize

        for node, distance in get_neighbors(src, keys):
            # call find_keys with the current source node removed from the list of keys to find
            dist = distance + find_keys(node, _update_keys(keys, src))
            if dist < best:
                best = dist

        return best

    return find_keys(START, '')


@time_it
def main(data_lines: list[str]) -> None:
    steps = collect_keys(data_lines)
    # pprint(steps)

    print(f'End result: {steps}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])

    # using test_data 0:
    #   End result: 8
    #   Finished 'main' in less than a millisecond
    # using test_data 1:
    #   End result: 86
    #   Finished 'main' in 4 milliseconds
    # using test_data 2:
    #   End result: 132
    #   Finished 'main' in 5 milliseconds
    # using test_data 3:
    #   End result: 136
    #   Finished 'main' in 1 second
    # using test_data 4:
    #   End result: 81
    #   Finished 'main' in 6 milliseconds
    # using input data:
    #   End result: 5392
    #   Finished 'main' in 9.4 seconds on work computer
    #   Finished 'main' in 5.8 seconds on home computer

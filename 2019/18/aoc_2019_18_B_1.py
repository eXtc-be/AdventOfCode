# aoc_2019_18_B_1.py - Day 18: Many-Worlds Interpretation - part 2
# After updating your map and using the remote-controlled robots,
# what is the fewest steps necessary to collect all the keys?
# https://adventofcode.com/2019/day/18
# based on the solution from aoc_2019_18_A_3, but with 4 starting points/mazes instead of 1


from aoc_2019_18_A_1 import (
    DATA_PATH,
    START, WALL, EMPTY, KEYS,
    Node,
    load_data,
    # test_data,
)

from aoc_2019_18_A_2 import (
    find_distance,
    Point,
)

from tools import time_it

from itertools import combinations
from functools import lru_cache
from sys import maxsize

from pprint import pprint


ROBOTS = '1234'


def change_grid(grid: list[str]) -> tuple[list[str], list[Node]]:
    """finds the START position and replaces it with 4 new starting positions and some walls"""
    new_grid = [[char for char in row] for row in grid]
    start_node = None
    start_nodes = []

    for r, row in enumerate(grid[1:-1], 1):
        for c, char in enumerate(row[1:-1], 1):
            if char == START:
                start_node = Node(r, c)
                break

    new_grid[start_node.row][start_node.col] = WALL

    for direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        new_grid[start_node.row + direction[0]][start_node.col + direction[1]] = WALL

    for i, direction in enumerate(((-1, -1), (-1, 1), (1, -1), (1, 1))):
        new_grid[start_node.row + direction[0]][start_node.col + direction[1]] = ROBOTS[i]
        start_nodes.append(Node(start_node.row + direction[0], start_node.col + direction[1]))

    return [''.join(row) for row in new_grid], start_nodes


@lru_cache(27)
def _update_keys(keys: str, new: str) -> str:
    # print(keys, new)
    return ''.join(sorted(set(list(keys) + [key for key in new if key in KEYS])))


def collect_keys(grid: list[str]) -> int | None:
    all_keys = ''
    points = []

    # find all points of interest (start, keys, doors)
    for r, row in enumerate(grid[1:-1], 1):
        for c, char in enumerate(row[1:-1], 1):
            if char in ROBOTS or char in KEYS:
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
            if (
                    distance < maxsize and
                    neighbor not in keys and
                    neighbor in all_keys and
                    all(door.lower() in keys + node for door in doors)
            ):
                neighbors.append((neighbor, distance))

        return neighbors

    # use precalculated paths to find all keys
    print('collecting keys')
    counter = 0

    @lru_cache(2 ** len(all_keys))
    def find_keys(sources: str, keys: str) -> int:
        if _update_keys(keys, sources) == all_keys:
            return 0

        best = maxsize

        for src in sources:
            for node, distance in get_neighbors(src, keys):
                # call find_keys with the current source node removed from the list of keys to find
                dist = distance + find_keys(sources.replace(src, node), _update_keys(keys, node))
                if dist < best:
                    best = dist

        return best

    return find_keys(ROBOTS, '')


test_data = [
'''
#######
#a.#..#
##...##
##.@.##
##...##
#..#Ab#
#######
'''.strip().splitlines(),
'''
#######
#bA#..#
##...##
##.@.##
##...##
#..#.a#
#######
'''.strip().splitlines(),
'''
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
'''.strip().splitlines(),
'''
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############
'''.strip().splitlines(),
'''
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
'''.strip().splitlines(),
'''
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
'''.strip().splitlines(),
]


@time_it
def main(data_lines: list[str]) -> None:
    grid, start_nodes = change_grid(data_lines)
    # print('\n'.join(grid))
    # pprint(start_nodes)

    steps = collect_keys(grid)

    print(f'End result: {steps}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0])
    # main(test_data[1])
    # main(test_data[2])
    # main(test_data[3])
    # main(test_data[4])
    # main(test_data[5])

    # using test_data 2:
    #   End result: 8
    #   Finished 'main' in 1 millisecond
    # using test_data 3:
    #   End result: 24
    #   Finished 'main' in 2 milliseconds
    # using test_data 4:
    #   End result: 32
    #   Finished 'main' in 8 milliseconds
    # using test_data 5:
    #   End result: 72
    #   Finished 'main' in 21 milliseconds
    # using input data:
    #   End result: 1684
    #   Finished 'main' in 11 seconds

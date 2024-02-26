# aoc_2017_12_A_1.py - Day 12: Digital Plumber - part 1
# How many programs are in the group that contains program ID 0?
# https://adventofcode.com/2017/day/12


from tools import time_it

from sys import maxsize

from pprint import pprint


DATA_PATH = './input_2017_12'

ROOT = 0


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_programs(data_lines: list[str]) -> dict[int, list[int]]:
    programs = {}

    for line in data_lines:
        program_id, connections = line.split(' <-> ')
        program_id = int(program_id)
        connections = [int(connection) for connection in connections.split(', ')]
        programs[program_id] = connections

    return programs


def get_distances(programs: dict[int, list[int]], root: int = ROOT) -> dict[int, int]:
    """Function that implements Dijkstra's single-source-shortest-path algorithm"""
    distances = {id: maxsize for id in programs}
    distances[root] = 0
    processed = {id: False for id in programs}

    for _ in range(len(programs)):
        # Pick the minimum distance vertex from the set of vertices not yet processed.
        # u is always equal to src in the first iteration
        u = min((distance, i) for i, distance in distances.items() if not processed[i])[1]

        # Put the minimum distance vertex in the processed list
        processed[u] = True

        # Update distances value of the adjacent vertices of the picked vertex only if the current
        # distance is greater than new distance and the vertex is not yet processed
        for v in programs:
            if v in programs[u] and not processed[v] and distances[v] > distances[u] + 1:
                distances[v] = distances[u] + 1

    return distances


test_data = '''
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    programs = get_programs(data_lines)
    # print(programs)

    distances = get_distances(programs, ROOT)
    # print(distances)

    connected = [program for program in programs if distances[program] < maxsize]
    # print(connected)

    print(f'End result: {len(connected)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 6
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 380
    #   Finished 'main' in 1 second

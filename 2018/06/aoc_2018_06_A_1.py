# aoc_2018_06_A_1.py - Day 6: Chronal Coordinates - part 1
# What is the size of the largest area that isn't infinite?
# https://adventofcode.com/2018/day/6


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2018_06'

# other constants


@dataclass
class Point:
    x: int
    y: int

    def distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class NamedPoint:
    name: str
    location: Point

    def __hash__(self):
        return hash(self.name)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_coords(data_lines: list[str]) -> list[NamedPoint]:
    # return [Point(*map(int, line.split(', '))) for line in data_lines]
    coords = []

    if len(data_lines) <= 26:
        current_name = 'a'
    else:
        current_name = 'aa'

    for line in data_lines:
        coords.append(NamedPoint(current_name, Point(*map(int, line.split(', ')))))
        if len(data_lines) <= 26:
            current_name = chr(ord(current_name[-1])+1)
        else:
            current_name = current_name[0] + chr(ord(current_name[-1])+1)
            if current_name[-1] == '{':
                current_name = chr(ord(current_name[0])+1) + 'a'

    return coords


def _get_distances(coords: list[NamedPoint], point: Point) -> dict[NamedPoint, int]:
    return {coord: coord.location.distance(point) for coord in coords}


def populate_grid(grid: list[list[str]], coords: list[NamedPoint]) -> None:
    for coord in coords:
        grid[coord.location.y][coord.location.x] = coord.name.upper()

    for row in range(max(coord.location.y for coord in coords) + 2):
        for col in range(max(coord.location.x for coord in coords) + 2):
            if Point(col, row) not in [coord.location for coord in coords]:  # skip the actual locations
                distances = _get_distances(coords, Point(col, row))
                closest = min(distances.items(), key=lambda item: item[1])
                if list(distances.values()).count(closest[1]) > 1:  # more than one location is close to this point
                    grid[row][col] = '.' * len(closest[0].name)
                else:  # point is equally distant from at least 2 points
                    grid[row][col] = closest[0].name


def _validate(grid: list[list[str]], name: str) -> int:
    count = 0

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell.lower() == name:
                if r == 0 or r == len(grid)-1 or c == 0 or c == len(grid[r])-1:
                    # any cell in grid that is on one of the edges of the grid indicates an infinite area
                    return -1
                count += 1

    return count


def find_areas(grid: list[list[str]], coords: list[NamedPoint]) -> dict[NamedPoint, int]:
    # areas = {}
    #
    # for coord in coords:
    #     areas[coord] = _validate(grid, coord.name)
    #
    # return areas
    #
    return {coord: _validate(grid, coord.name) for coord in coords}


test_data = '''
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    coords = get_coords(data_lines)
    # pprint(coords)

    placeholder = '_'
    if len(data_lines) > 26:
        placeholder = '__'

    grid = [
        [placeholder for _ in range(max(coord.location.x for coord in coords)+2)]
        for _ in range(max(coord.location.y for coord in coords)+2)
    ]
    # pprint(grid, width=(max(coord.location.x for coord in coords)+1)*7)

    populate_grid(grid, coords)
    # pprint(grid, width=(max(coord.location.x for coord in coords)+1)*7)
    # print('\n'.join(''.join(cell for cell in row) for row in grid))

    areas = find_areas(grid, coords)
    # pprint(areas)

    print(f'End result: {max(areas.values())}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 17
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 3293
    #   Finished 'main' in 4.7 seconds

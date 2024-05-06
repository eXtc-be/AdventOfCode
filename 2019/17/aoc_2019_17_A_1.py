# aoc_2019_17_A_1.py - Day 17: Set and Forget - part 1
# Run your ASCII program. What is the sum of the alignment parameters for the scaffold intersections?
# https://adventofcode.com/2019/day/17


from tools import time_it

from dataclasses import dataclass

from pprint import pprint


DATA_PATH = './input_2019_17'

SCAFFOLD = '#'
EMPTY = '.'


@dataclass
class Coord:
    x: int = 0
    y: int = 0

    def distance(self, other: 'Coord' = None) -> int:
        other = Coord(0, 0) if other is None else other
        return abs(self.x - other.x) + abs(self.y - other.y)

    @property
    def alignment(self) -> int:
        return self.x * self.y

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __hash__(self) -> int:
        return hash((self.x, self.y))


HEADINGS = (
    Coord(0, -1),  # up
    Coord(0, 1),   # down
    Coord(-1, 0),  # left
    Coord(1, 0),   # right
)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_scaffolding_data() -> list[str]:
    from intcode import Computer

    computer = Computer(list(map(int, load_data(DATA_PATH)[0].split(','))), [], False)
    computer.run()
    return ''.join(chr(number) for number in computer.outputs).strip().splitlines()


def find_intersections(data_lines: list[str]) -> list[Coord]:
    # because an intersection must have 4 neighbours we can exclude first and last lines and columns
    # this also means we don't have to check boundaries
    intersections = []

    for r, row in enumerate(data_lines[1:-1], 1):
        for c, char in enumerate(row[1:-1], 1):
            if char == SCAFFOLD:
                if all(data_lines[r+direction.y][c+direction.x] == SCAFFOLD for direction in HEADINGS):
                    intersections.append(Coord(c, r))

    return intersections


test_data = '''
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    print('\n'.join(data_lines))

    intersections = find_intersections(data_lines)
    # pprint(intersections)

    # pprint([intersection.alignment for intersection in intersections])

    print(f'End result: {sum([intersection.alignment for intersection in intersections])}')


if __name__ == "__main__":
    main(get_scaffolding_data())
    # main(test_data)

    # using test_data:
    #   End result: 76
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 7404
    #   Finished 'main' in less than a millisecond

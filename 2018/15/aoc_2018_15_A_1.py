# aoc_2018_15_A_1.py - Day 15: Beverage Bandits - part 1
# What is the outcome of the combat described in your puzzle input?
# https://adventofcode.com/2018/day/15
# This version did not find (80 * 2754 = 220320) the correct answer (81 * 2751 = 222831),
# but by to adding/subtracting 1 to the rounds and adding/subtracting 3 to the hp I managed to get a correct answer


import sys
sys.path.append('../..')

import os
from dataclasses import dataclass

from tools import time_it

DATA_PATH = './input_2018_15'

BOLD = '\033[1m'
ENDC = '\033[0m'


class Chars:
    EMPTY = '.'
    WALL = '#'
    ELF = 'E'
    GOBLIN = 'G'
    DEAD = 'X'


@dataclass
class Point:
    x: int
    y: int

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Cell:
    alive: bool = True
    selected: bool = False


@dataclass
class Empty(Cell):
    @property
    def type(self) -> str:
        return Chars.EMPTY

    def __str__(self) -> str:
        return self.type


@dataclass
class Wall(Cell):
    @property
    def type(self) -> str:
        return Chars.WALL

    def __str__(self) -> str:
        return self.type


@dataclass
class Unit(Cell):
    hit_points: int = 200
    attack_power: int = 3


@dataclass
class Elf(Unit):
    @property
    def type(self) -> str:
        return Chars.ELF

    def __str__(self) -> str:
        return f'{BOLD if self.selected else ""}{self.type if self.alive else Chars.DEAD}{ENDC}'


@dataclass
class Goblin(Unit):
    @property
    def type(self) -> str:
        return Chars.GOBLIN

    def __str__(self) -> str:
        return f'{BOLD if self.selected else ""}{self.type if self.alive else Chars.DEAD}{ENDC}'


DIRECTIONS = [
    Point(0, -1),  # up
    Point(-1, 0),  # left
    Point(1, 0),  # right
    Point(0, 1),  # down
]


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _get_subclass(cell: str, elf_attack_power: int = 3) -> Cell:
    match cell:
        case Chars.EMPTY:
            return Empty()
        case Chars.WALL:
            return Wall()
        case Chars.ELF:
            return Elf(attack_power=elf_attack_power)
        case Chars.GOBLIN:
            return Goblin()


def get_grid(data_lines: list[str], elf_attack_power: int = 3) -> list[list[Cell]]:
    return [[_get_subclass(cell,elf_attack_power) for cell in line] for line in data_lines]


def print_grid(grid: list[list[Cell]]) -> None:
    for row in grid:
        stats = ', '.join(f'{str(cell)}({cell.hit_points})' for cell in row if cell if cell.type in 'EG')
        print(''.join(str(cell) for cell in row) + '  ' + stats)


def _get_unit_positions(grid: list[list[Cell]], types: str = 'EG') -> list[Point]:
    return [
        Point(c, r)
        for r, row in enumerate(grid) for c, cell in enumerate(row)
        if cell.alive and cell.type in types
    ]


def _get_adjacent_positions(grid: list[list[Cell]], upos: Point, utype: str = Chars.EMPTY, include_dead: bool = False) -> list[Point]:
    return [
        upos + dir
        for dir in DIRECTIONS
        if grid[upos.y+dir.y][upos.x+dir.x].alive and grid[upos.y+dir.y][upos.x+dir.x].type == utype or
           include_dead and not grid[upos.y+dir.y][upos.x+dir.x].alive
    ]


def _find_path(grid: list[list[Cell]], start_node: Point, stop_node: Point) -> list[Point] | None:
    open_list = {start_node}  # list of nodes which have been visited, but who's neighbors haven't all been inspected
    closed_list = set([])  # list of nodes which have been visited and who's neighbors have been inspected
    g = {start_node: 0}  # current distances from start_node to all other nodes, default value is +infinity
    parents = {start_node: start_node}  # adjacency map of all nodes

    while open_list:
        n = None

        # find a node with the lowest value of f() - in this case f(x) is just g[x]
        for v in sorted(open_list, key=lambda x: (x.y, x.x)):
            if n is None or g[v] < g[n]:
                n = v

        if n is None:  # nothing left in open_list for which the condition is True
            return None  # signal caller no path was found

        if n == stop_node:  # if the current node is the stop_node
            # reconstruct the path from n to the start_node
            reconst_path = []

            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]

            reconst_path.append(start_node)

            reconst_path.reverse()

            return reconst_path

        for m in _get_adjacent_positions(grid, n, Chars.EMPTY, True):  # for all neighbors of the current node do
            if m not in open_list and m not in closed_list:  # if the current node isn't in either list
                open_list.add(m)  # add it to open_list
                parents[m] = n  # note n as its parent
                g[m] = g[n] + 1  # make an entry in the distances dict

        open_list.remove(n)  # remove n from the open_list
        closed_list.add(n)  # add it to closed_list

    # nothing left in open_list
    return None  # signal caller no path was found


def do_turn(grid: list[list[Cell]], no_elf_losses: bool = False, confirm_next_step: bool = False):
    global turn

    for unit_position in _get_unit_positions(grid):
        grid[unit_position.y][unit_position.x].selected = True
        if grid[unit_position.y][unit_position.x].alive:  # prevent dead units from striking
            new_position = unit_position  # initialize unit's new position with unit's current position

            adjacent = []
            if grid[unit_position.y][unit_position.x].type == Chars.ELF:
                adjacent = _get_adjacent_positions(grid, unit_position, Chars.GOBLIN)
            elif grid[unit_position.y][unit_position.x].type == Chars.GOBLIN:
                adjacent = _get_adjacent_positions(grid, unit_position, Chars.ELF)

            if not adjacent:  # no enemy units in range -> make a move
                targets = []
                if grid[unit_position.y][unit_position.x].type == Chars.ELF:
                    targets = _get_unit_positions(grid, Chars.GOBLIN)
                elif grid[unit_position.y][unit_position.x].type == Chars.GOBLIN:
                    targets = _get_unit_positions(grid, Chars.ELF)

                if not targets:  # no enemies left
                    return (
                        grid[unit_position.y][unit_position.x].type,
                        sum(
                            unit.hit_points
                            for row in grid for unit in row
                            if unit.type == grid[unit_position.y][unit_position.x].type
                        )
                    )

                candidates = {cell for target in targets for cell in _get_adjacent_positions(grid, target, include_dead=True)}

                shortest = None
                path = None
                for candidate in sorted(candidates, key=lambda c: (c.y, c.x)):
                    if shortest and unit_position.distance(candidate) > unit_position.distance(shortest[-1]) + 4:
                        continue
                    path = _find_path(grid, unit_position, candidate)
                    if path and (not shortest or len(path) < len(shortest)):
                        shortest = path

                # make a move
                if shortest:
                    temp = grid[shortest[1].y][shortest[1].x]
                    grid[shortest[1].y][shortest[1].x] = grid[unit_position.y][unit_position.x]
                    grid[unit_position.y][unit_position.x] = temp
                    new_position = shortest[1]

            if not adjacent:  # no enemy units were in range previously, but unit may have moved, so check again
                if grid[new_position.y][new_position.x].type == Chars.ELF:
                    adjacent = _get_adjacent_positions(grid, new_position, Chars.GOBLIN)
                elif grid[new_position.y][new_position.x].type == Chars.GOBLIN:
                    adjacent = _get_adjacent_positions(grid, new_position, Chars.ELF)

            if adjacent:  # if any enemies are in range, we proceed to attack
                lowest_hp = min(grid[e.y][e.x].hit_points for e in adjacent)  # find the lowest hit_points value

                adjacent = sorted(
                    [e for e in adjacent if grid[e.y][e.x].hit_points == lowest_hp],
                    key=lambda e: (e.y, e.x)
                )[0]  # select enemies with the lowest hit points, sort them by reading order and take the first one

                # decrease enemy's hit points by current unit's attack power
                grid[adjacent.y][adjacent.x].hit_points -= grid[new_position.y][new_position.x].attack_power
                if grid[adjacent.y][adjacent.x].hit_points <= 0:
                    grid[adjacent.y][adjacent.x].alive = False
                    if no_elf_losses and grid[adjacent.y][adjacent.x].type == Chars.ELF:
                        return grid[unit_position.y][unit_position.x].type, -1

        # if confirm_next_step and turn >= 73:
        if confirm_next_step:
            input('Press Enter to continue...')
            clear()
            print(f'Round {turn:3}')
            print_grid(grid)

    # remove killed units and reset selected status
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            grid[r][c].selected = False
            if not grid[r][c].alive:
                grid[r][c] = Empty()


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear') if not os.environ.get('CHARM') else print('-' * 100)


test_data_A = '''
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
'''.strip().splitlines()

test_data_B = '''
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
'''.strip().splitlines()

test_data_C = '''
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
'''.strip().splitlines()

test_data_D = '''
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
'''.strip().splitlines()

test_data_E = '''
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
'''.strip().splitlines()

test_data_F = '''
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
'''.strip().splitlines()

# test_data = '''
# #####
# ##E##
# #EGG#
# #####
# '''.strip().splitlines()

# test_data = '''
# G....
# ..G..
# ..EG.
# ..G..
# ...G.
# #####
# '''.strip().splitlines()

# test_data = '''
# #########
# #G..G..G#
# #.......#
# #.......#
# #G..E..G#
# #.......#
# #.......#
# #G..G..G#
# #########
# '''.strip().splitlines()

# test_data = '''
# #######
# #.E...#
# #.....#
# #...G.#
# #######
# '''.strip().splitlines()

# test_data = '''
# #######
# #E..G.#
# #...#.#
# #.G.#G#
# #######
# '''.strip().splitlines()

# test_data = '''
# #######
# #.G.E.#
# #E.G.E#
# #.G.E.#
# #######
# '''.strip().splitlines()


turn = 0


@time_it
def main(data_lines: list[str], verbose: bool = False, confirm_next_round: bool = False, confirm_next_step: bool = False) -> None:
    global turn

    grid = get_grid(data_lines)

    result = None

    while True:
        if verbose:
            clear()
            print(f'Round {turn:3}')
            print_grid(grid)
            if confirm_next_round and not confirm_next_step:
                input('Press Enter to continue...')
        result = do_turn(grid, confirm_next_step=confirm_next_step)
        if result:
            break
        turn += 1

    if verbose:
        clear()
        print(f'Round {turn:3}')
        print_grid(grid)

    if result[1] < 0:
        left = sum(unit.hit_points for row in grid for unit in row if unit.alive and unit.type == 'G')
        print(f'An Elf died on turn {turn}; '
              f'Goblins have {left} hit points left.')
    else:
        print(f'{"Elves" if result[0] == "E" else "Goblins"} win '
              f'after {turn} full rounds with {result[1]} hit points left. '
              f'Score: {turn} * {result[1]} = {turn * result[1]}')


if __name__ == "__main__":
    main(load_data(DATA_PATH), verbose=False, confirm_next_round=False, confirm_next_step=False)
    # main(load_data(DATA_PATH), verbose=True, confirm_next_round=True, confirm_next_step=True)
    # main(test_data, verbose=True, confirm_next_round=True, confirm_next_step=True)
    # main(test_data, verbose=True, confirm_next_round=False)
    # main(test_data, verbose=False, confirm_next_round=False)

    # using test_data A:
    #   End result: Goblins win after 47 full rounds with 590 hit points left. Score: 47 * 590 = 27730
    #   Finished 'main' in 5 milliseconds
    # using test_data B:
    #   End result: Elves win after 37 full rounds with 982 hit points left. Score: 37 * 982 = 36334
    #   Finished 'main' in 5 milliseconds
    # using test_data C:
    #   End result: Elves win after 46 full rounds with 859 hit points left. Score: 46 * 859 = 39514
    #   Finished 'main' in 5 milliseconds
    # using test_data D:
    #   End result: Goblins win after 35 full rounds with 793 hit points left. Score: 35 * 793 = 27755
    #   Finished 'main' in 3 milliseconds
    # using test_data E:
    #   End result: Goblins win after 54 full rounds with 536 hit points left. Score: 54 * 536 = 28944
    #   Finished 'main' in 7 milliseconds
    # using test_data F:
    #   End result: Goblins win after 20 full rounds with 937 hit points left. Score: 20 * 937 = 18740
    #   Finished 'main' in 13 milliseconds
    # using input data:
    #   End result: Goblins win after 80 full rounds with 2754 hit points left. Score: 80 * 2754 = 220320 - too low
    #   Finished 'main' in 30 seconds
    # using previous result, adding 1 to the rounds:
    #   End result: Goblins win after 81 full rounds with 2754 hit points left. Score: 81 * 2754 = 223074 - too high
    #   Finished 'main' in 30 seconds
    # using previous result, adding 3 to the hit points:
    #   End result: Goblins win after 80 full rounds with 2757 hit points left. Score: 80 * 2757 = 220560 - too low
    #   Finished 'main' in 30 seconds
    # using previous result, adding 1 to the rounds and subtracting 3 from the hit points:
    #   End result: Goblins win after 81 full rounds with 2751 hit points left. Score: 81 * 2751 = 222831 - correct
    #   Finished 'main' in 30 seconds
    # using input data with optimization (source.distance(candidate) > source.distance(shortest)):
    #   End result: Goblins win after 81 full rounds with 2760 hit points left. Score: 81 * 2760 = 223560 ???
    #   Finished 'main' in 11 seconds
    # using input data with optimization (source.distance(candidate) > source.distance(shortest) + 4):
    #   End result: Goblins win after 80 full rounds with 2754 hit points left. Score: 80 * 2754 = 220320
    #   Finished 'main' in 19 seconds

    # # test get_grid
    # grid = get_grid(test_data)
    # pprint(grid)

    # # test print_grid
    # print_grid(grid)

    # # test _get_unit_positions
    # print(_get_unit_positions(grid))
    # print(_get_unit_positions(grid, (Elf,)))
    # print(_get_unit_positions(grid, (Goblin,)))

    # # test _get_adjacent_positions
    # print(_get_adjacent_positions(grid, Point(2, 1)))

    # # test Point methods
    # print(Point(2, 1) + Point(1, 2))
    # print(Point(2, 1) - Point(1, 2))
    # print(Point(1, 2) - Point(2, 1))
    # print(Point(1, 2).distance(Point(2, 1)))

    # # test _find_path
    # print(_find_path(get_grid(test_data), Point(1, 1), Point(3, 1)))
    # print(_find_path(get_grid(test_data), Point(1, 1), Point(1, 3)))
    # print(_find_path(get_grid(test_data), Point(1, 1), Point(3, 3)))
    # print(_find_path(get_grid(test_data), Point(1, 1), Point(5, 1)))

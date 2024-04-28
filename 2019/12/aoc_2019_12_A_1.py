# aoc_2019_12_A_1.py - Day 12: The N-Body Problem - part 1
# What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
# https://adventofcode.com/2019/day/12


from tools import time_it, evalPlural

from dataclasses import dataclass, field
from itertools import combinations

from pprint import pprint


DATA_PATH = './input_2019_12'

STEPS = 1000

WIDTH = 3


@dataclass
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    def distance(self, other: 'Point' = None) -> int:
        other = Point(0, 0, 0) if other is None else other
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f'<x={self.x:{WIDTH}}, y={self.y:{WIDTH}}, z={self.z:{WIDTH}}>'

    def __hash__(self):
        return hash((self.x, self.y, self.z))


@dataclass
class Moon:
    position: Point
    velocity: Point = field(default_factory=Point)

    def __str__(self):
        return f'pos={self.position}, vel={self.velocity}'

    def __hash__(self):
        return hash((self.position, self.velocity))


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_moons(data_lines: list[str]) -> list[Moon]:
    return [Moon(Point(*[int(part.split('=')[-1]) for part in line[1:-1].split(', ')])) for line in data_lines]


def update_velocities(moons: list[Moon]) -> list[Moon]:
    for first, second in combinations(moons, 2):
        if first.position.x > second.position.x:
            first.velocity.x -= 1
            second.velocity.x += 1
        elif first.position.x < second.position.x:
            first.velocity.x += 1
            second.velocity.x -= 1
        else:  # first.x == second.x
            pass

        if first.position.y > second.position.y:
            first.velocity.y -= 1
            second.velocity.y += 1
        elif first.position.y < second.position.y:
            first.velocity.y += 1
            second.velocity.y -= 1
        else:  # first.x == second.x
            pass

        if first.position.z > second.position.z:
            first.velocity.z -= 1
            second.velocity.z += 1
        elif first.position.z < second.position.z:
            first.velocity.z += 1
            second.velocity.z -= 1
        else:  # first.x == second.x
            pass

    return moons


def apply_velocities(moons: list[Moon]) -> list[Moon]:
    for moon in moons:
        moon.position.x += moon.velocity.x
        moon.position.y += moon.velocity.y
        moon.position.z += moon.velocity.z

    return moons


def do_step(moons: list[Moon]) -> list[Moon]:
    moons = update_velocities(moons)
    moons = apply_velocities(moons)
    return moons


def print_moons(moons: list[Moon], step: int) -> None:
    print('After %d step%s:' % evalPlural(step))
    for moon in moons:
        print(f'{moon}')


def print_energy(moons: list[Moon], step: int) -> None:
    total = 0

    print('Energy after %d step%s:' % evalPlural(step))
    for moon in moons:
        pot = moon.position.distance()
        kin = moon.velocity.distance()
        print(f'pot:{pot:{WIDTH}};   kin:{kin:{WIDTH}};   total:{pot*kin:{WIDTH}}')
        total += pot * kin

    print(f'Sum of total energy: {total}')


test_data = [
'''
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
'''.strip().splitlines(),
'''
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
'''.strip().splitlines(),
]


@time_it
def main(data_lines: list[str], steps: int = STEPS, verbose: bool = False, confirm: bool = False) -> None:
    moons = get_moons(data_lines)

    if verbose:
        print_moons(moons, 0)
        print_energy(moons, 0)
        if confirm:
            input()
        else:
            print()

    for step in range(1, steps+1):
        moons = do_step(moons)

        if verbose:
            print_moons(moons, step)
            print_energy(moons, step)
            if confirm:
                input()
            else:
                print()

    print(f'End result: {sum(moon.position.distance() * moon.velocity.distance() for moon in moons)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data[0], 10)
    # main(test_data[1], 100)

    # using test_data 0, 10 steps:
    #   End result: 179
    #   Finished 'main' in less than a millisecond
    # using test_data 1, 100 steps:
    #   End result: 1940
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 5937
    #   Finished 'main' in 4 milliseconds

    # moons = [
    #     Moon(Point(3, 3, 3)),
    #     Moon(Point(5, 5, 5)),
    # ]
    # moons = update_velocities(moons)
    # pprint(moons)
    #
    # moons = apply_velocities(moons)
    # pprint(moons)

# aoc_2017_20_A_1.py - Day 20: Particle Swarm - part 1
# Which particle will stay closest to position <0,0,0> in the long term?
# https://adventofcode.com/2017/day/20
# strategy 1: do the simulation with 'enough' rounds and see which particle has
#             the lowest manhattan distance to the origin
#             -> what is enough ? (turns out about 500 rounds is enough to get the correct answer)


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2017_20'

ROUNDS = 5000
ROUNDS_TEST = 3


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Particle:
    position: Vector
    velocity: Vector
    acceleration: Vector

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    @property
    def manhattan(self):
        return self.position.manhattan


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_particles(data_lines: list[str]) -> list[Particle]:
    return [
        Particle(
            Vector(*(int(el) for el in line.split(', ')[0][3:-1].split(','))),
            Vector(*(int(el) for el in line.split(', ')[1][3:-1].split(','))),
            Vector(*(int(el) for el in line.split(', ')[2][3:-1].split(','))),
        )
        for line in data_lines
    ]


def run_simulation(particles: list[Particle]) -> None:
    for particle in particles:
        particle.update()


test_data = '''
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    particles = get_particles(data_lines)
    # pprint(particles)

    for _ in range(rounds):
        # print('-' * 100)
        run_simulation(particles)
        # print([(particle.position, particle.manhattan) for particle in particles])

    distance, id = min((particle.manhattan, i) for i, particle in enumerate(particles))

    print(f'End result: {id=}, {distance=:,}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, ROUNDS_TEST)
    # using test_data:
    #   End result: 0
    #   Finished 'main' in less than a millisecond
    # using input data using 5000, 10000, 100000, 1000, 500 rounds:
    #   End result: 276 - too high
    #   Finished 'main' in 7.3 seconds,..
    # using input data using 100 rounds:
    #   End result: 89 - incorrect
    #   Finished 'main' in xxx

# aoc_2017_20_A_2.py - Day 20: Particle Swarm - part 1
# Which particle will stay closest to position <0,0,0> in the long term?
# https://adventofcode.com/2017/day/20
# strategy 2: - find the particle(s) with the lowest absolute value
#             - in case of a tie, find the one(s) with lowest absolute starting velocity
#             - if there is still a tie, find the one(s) with the lowest absolute starting position


from tools import time_it

from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2017_20'

# other constants


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
    id: int
    position: Vector
    velocity: Vector
    acceleration: Vector

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_particles(data_lines: list[str]) -> list[Particle]:
    return [
        Particle(
            id,
            Vector(*(int(el) for el in line.split(', ')[0][3:-1].split(','))),
            Vector(*(int(el) for el in line.split(', ')[1][3:-1].split(','))),
            Vector(*(int(el) for el in line.split(', ')[2][3:-1].split(','))),
        )
        for id, line in enumerate(data_lines)
    ]


test_data = '''
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    particles = get_particles(data_lines)
    # pprint(particles)

    lowest_a = min(abs(particle.acceleration.manhattan) for particle in particles)
    lowest_acc = [particle for particle in particles if particle.acceleration.manhattan == lowest_a]
    # pprint(lowest_acc)
    # print('-' * 100)

    lowest_v = min(abs(particle.velocity.manhattan) for particle in lowest_acc)
    lowest_vel = [particle for particle in lowest_acc if particle.velocity.manhattan == lowest_v]
    # pprint(lowest_vel)
    # print('-' * 100)

    lowest_p = min(abs(particle.position.manhattan) for particle in lowest_vel)
    lowest_pos = [particle for particle in lowest_vel if particle.position.manhattan == lowest_p]
    # pprint(lowest_pos)

    print(f'End result: {lowest_pos[0].id}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 0
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 91
    #   Finished 'main' in 10 milliseconds

    # # test Vector.manhattan
    # print(Vector(x=0, y=0, z=0).manhattan)
    # print(Vector(x=0, y=-3, z=0).manhattan)

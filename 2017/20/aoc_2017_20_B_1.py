# aoc_2017_20_B_1.py - Day 20: Particle Swarm - part 2
# How many particles are left after all collisions are resolved?
# https://adventofcode.com/2017/day/20
# brute force method: do enough rounds and count the remaining particles, hoping all collisions are resolved
# I got the correct answer for my input with 500 rounds first try, but could get as low as 39 to get the same answer


from aoc_2017_20_A_1 import (
    DATA_PATH,
    ROUNDS,
    ROUNDS_TEST,
    Particle,
    load_data,
    # test_data,
    get_particles,
    run_simulation,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def remove_collided(particles: list[Particle]) -> None:
    candidates = [particle for particle in particles]

    while candidates:
        particle = candidates[0]
        to_remove = [p for p in candidates if p.position == particle.position]
        for p in to_remove:
            candidates.remove(p)
            if len(to_remove) > 1:
                particles.remove(p)


test_data = '''
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], rounds: int = ROUNDS) -> None:
    particles = get_particles(data_lines)
    # pprint(particles)

    for _ in range(rounds):
        run_simulation(particles)
        # print([particle.position for particle in particles])
        remove_collided(particles)
        # print([particle.position for particle in particles])
        # print('-' * 100)

    print(f'End result: {len(particles)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines, 39)
    # main(data_lines, ROUNDS_TEST)
    # using test_data:
    #   End result: 1
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 567
    #   Finished 'main' in 9.2 seconds

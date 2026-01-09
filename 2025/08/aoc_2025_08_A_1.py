# aoc_2025_08_A_1.py - Day 8: Playground - part 1
# Your list contains many junction boxes; connect together the 1000 pairs of
# junction boxes which are closest together. Afterward, what do you get if
# you multiply together the sizes of the three largest circuits?
# https://adventofcode.com/2025/day/8

from tools import time_it

# other imports

from pprint import pprint
from dataclasses import dataclass, field
from itertools import combinations
from math import sqrt, prod
from collections import namedtuple
from contextlib import suppress


DATA_PATH = './input_2025_08'

# other constants


# classes
Junction = namedtuple('Junction', 'x y z')


@dataclass
class Circuit():
    junctions: list[Junction] = field(default_factory=list)


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions
def get_junctions(lines: list[str]) -> list[Junction]:
    return [Junction(*[int(part) for part in line.split(',')]) for line in lines]


def get_distances(junctions: list[Junction]) -> dict[tuple[Junction, Junction], float]:
    return {(p1, p2): calc_distance(p1, p2) for p1, p2 in combinations(junctions, 2)}


def calc_distance(p1: Junction, p2: Junction) -> float:
    return sqrt(sum((c2 - c1) ** 2 for c1, c2 in zip(p1, p2)))


def find_circuit(circuits: list[Circuit], junction: Junction) -> Circuit | None:
    for circuit in circuits:
        if junction in circuit.junctions:
            return circuit
    return None


def merge_circuits(circuit_1: Circuit, circuit_2: Circuit) -> Circuit:
    circuit_1.junctions += [junction for junction in circuit_2.junctions if junction not in circuit_1.junctions]
    return circuit_1


test_data = '''
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], pairs: int) -> None:
    junctions = get_junctions(data_lines)
    distances = get_distances(junctions)
    circuits = [Circuit([junction]) for junction in junctions]

    for pair in sorted(distances, key=lambda x: distances[x])[:pairs]:
        circuit_1 = find_circuit(circuits, pair[0])
        circuit_2 = find_circuit(circuits, pair[1])
        if circuit_1 != circuit_2:
            merge_circuits(circuit_1, circuit_2)
            circuits.remove(circuit_2)

    result = prod(
        len(circuit.junctions)
        for circuit in sorted(circuits, key=lambda x: len(x.junctions), reverse=True)[:3]
    )

    print(f'End result: {result}')


if __name__ == "__main__":
    # main(load_data(DATA_PATH), 1000)
    main(test_data, 10)

    # using test_data:
    #   End result: 40
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 90036
    #   Finished 'main' in 1.05 seconds

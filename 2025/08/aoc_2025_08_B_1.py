# aoc_2025_08_B_1.py - Day 8: Playground - part 2
# Continue connecting the closest unconnected pairs of junction boxes
# together until they're all in the same circuit. What do you get if you
# multiply together the X coordinates of the last two junction boxes you need
# to connect?
# https://adventofcode.com/2025/day/8


from aoc_2025_08_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_junctions,
    get_distances,
    Circuit,
    find_circuit,
    merge_circuits,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


# other functions


@time_it
def main(data_lines: list[str]) -> None:
    junctions = get_junctions(data_lines)
    distances = get_distances(junctions)
    circuits = [Circuit([junction]) for junction in junctions]
    last_pair = ()

    for pair in sorted(distances, key=lambda x: distances[x]):
        circuit_1 = find_circuit(circuits, pair[0])
        circuit_2 = find_circuit(circuits, pair[1])
        if circuit_1 != circuit_2:
            if len(circuits) == 2:  # found the last 2 junctions to make a single circuit
                last_pair = pair
                break
            merge_circuits(circuit_1, circuit_2)
            circuits.remove(circuit_2)

    result = last_pair[0].x * last_pair[1].x

    print(f'End result: {result}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 25272
    #   Finished 'main' in 1 millisecond
    # using input data:
    #   End result: 6083499488
    #   Finished 'main' in 1.25 seconds

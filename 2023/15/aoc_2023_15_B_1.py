# aoc_2023_15_B_1.py - Day 15: Lens Library - part 2
# Run the HASH algorithm on each step in the initialization sequence. What is the sum of the results? (The initialization sequence is one long line; be careful when copy-pasting it.)
# https://adventofcode.com/2023/day/15


from aoc_2023_15_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    calculate_hash,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def calculate_hashmap(seq: list[str]) -> dict[int, list[dict[str, int]]]:
    boxes = {i: [] for i in range(256)}
    # pprint(boxes);

    for step in seq:
        if '=' in step:
            label, focal_length = step.split('=')
            focal_length = int(focal_length)

            box_number = calculate_hash(label)

            if label in [k for lens in boxes[box_number] for k in lens.keys()]:  # a list of all keys in the list
                boxes[box_number] = [
                    lens
                    if lens.get(label) is None  # will yield a value for the one dict with this label, else None
                    else {label: focal_length}  # replace dict with key==label with a new value for focal_length
                    for lens in boxes[box_number]
                ]
            else:
                boxes[box_number].append({label: focal_length})
        elif step[-1] == '-':
            label = step[:-1]

            box_number = calculate_hash(label)

            if label in [k for lens in boxes[box_number] for k in lens.keys()]:  # a list of all keys in the list
                # replace list of lenses with previous list without the one labeled with label
                boxes[box_number] = [
                    lens
                    for lens in boxes[box_number]
                    if lens.get(label) is None  # will yield a value for the one dict with this label, else None
                ]

    return boxes


def calc_focussing_powers(boxes: dict[int, list[dict[str, int]]]) -> list[list[int]]:
    focussing_powers = []

    for num, box in enumerate(boxes.values(), 1):
        powers = []
        for slot, lens in enumerate(box, 1):
            powers.append(num * slot * sum(focus_length for focus_length in lens.values()))

        focussing_powers.append(powers)

    return focussing_powers


@time_it
def main(data_lines: list[str]) -> None:
    hashmap = calculate_hashmap(data_lines[0].split(','))
    # pprint(hashmap)

    focussing_powers = calc_focussing_powers(hashmap)
    # pprint(focussing_powers)

    print(f'End result: {sum(sum(powers) for powers in focussing_powers)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 145
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 215827
    #   Finished 'main' in 6 milliseconds

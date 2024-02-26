# aoc_2017_13_B_1.py - Day 13: Packet Scanners - part 2
# What is the fewest number of picoseconds that you need to delay the packet
# to pass through the firewall without being caught?
# https://adventofcode.com/2017/day/13


from aoc_2017_13_A_1 import (
    DATA_PATH,
    load_data,
    test_data,
    get_layers,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def is_caught(layers: dict[int: int], time: int = None, delta: int = 0) -> bool:
    max_layer = max(layers.keys()) + 1
    for layer in layers:
        if time % max_layer == layer:  # packet is in current layer
            # calculate position of current scanner
            r_pos = (time + delta) % (layers[layer] * 2 - 2)
            v_pos = r_pos + (layers[layer] - r_pos - 1) * 2 * (r_pos // layers[layer])
            if v_pos == 0:  # scanner is at position 0 -> caught
                return True

    # no packet was caught at this time
    return False


@time_it
def main(data_lines: list[str]) -> None:
    layers = get_layers(data_lines)
    # pprint(layers)

    delta = 0
    while True:
        if delta % 100_000 == 0:
            print(f'{delta:,}')

        caught = None
        for time in range(max(layers.keys()) + 1):
            if caught := is_caught(layers, time, delta):
                break

        # if, after checking a full run of the packet, it still isn't caught, we have a winner
        if not caught:
            break

        delta += 1

    print(f'End result: {delta}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 10
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 3865118
    #   Finished 'main' in 36 seconds

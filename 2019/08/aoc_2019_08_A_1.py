# aoc_2019_08_A_1.py - Day 8: Space Image Format - part 1
# On the layer that contains the fewest 0 digits,
# what is the number of '1' digits multiplied by the number of '2' digits?
# https://adventofcode.com/2019/day/8


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2019_08'

WIDTH, HEIGHT = 25, 6


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_raw_data(data: str) -> list[int]:
    return list(map(int, data))


def extract_layers(raw_data: list[int], width: int = WIDTH, height: int = HEIGHT) -> list[list[int]]:
    return [raw_data[pos:pos +  width * height] for pos in range(0, len(raw_data), width * height)]


test_data = '''
123456789012
'''.strip().splitlines()


@time_it
def main(data: str, width: int = WIDTH, height: int = HEIGHT) -> None:
    raw_data = get_raw_data(data)
    # pprint(raw_data)

    layers = extract_layers(raw_data, width, height)
    # pprint(layers)

    lowest_0 = min(layers, key=lambda l: l.count(0))
    # print(lowest_0)

    print(f'End result: {lowest_0.count(1) * lowest_0.count(2)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], 3, 2)

    # using test_data:
    #   End result: 1
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 2904
    #   Finished 'main' in 2 milliseconds

# aoc_2019_08_B_1.py - Day 8: Space Image Format - part 2
# What message is produced after decoding your image?
# https://adventofcode.com/2019/day/8


from aoc_2019_08_A_1 import (
    DATA_PATH,
    WIDTH,
    HEIGHT,
    load_data,
    get_raw_data,
    extract_layers,
    # test_data,
)

from tools import time_it

# other imports

from pprint import pprint


IMAGE = '.#'


def combine_layers(layers: list[list[int]], width: int = WIDTH, height: int = HEIGHT) -> list[list[int]]:
    image: list[list[int]] = [[None for _ in range(width)] for _ in range(height)]

    for layer in reversed(layers):
        for row in range(height):
            for col in range(width):
                if layer[row * width + col] != 2:
                    image[row][col] = layer[row * width + col]

    return image


def draw_image(image: list[list[int]]) -> None:
    print('\n'.join([''.join([IMAGE[c] for c in row]) for row in image]))


test_data = '''
0222112222120000
'''.strip().splitlines()


@time_it
def main(data: str, width: int = WIDTH, height: int = HEIGHT) -> None:
    raw_data = get_raw_data(data)
    # pprint(raw_data)

    layers = extract_layers(raw_data, width, height)
    # pprint(layers)

    image = combine_layers(layers, width, height)
    # pprint(image)
    draw_image(image)

    # print(f'End result: {lowest_0.count(1) * lowest_0.count(2)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH)[0])
    # main(test_data[0], 2, 2)

    # using input data:
    #   End result: HGBCF
    #   Finished 'main' in 3 milliseconds

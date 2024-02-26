# aoc_2017_13_A_1.py - Day 13: Packet Scanners - part 1
# Given the details of the firewall you've recorded, if you leave immediately,
# what is the severity of your whole trip?
# https://adventofcode.com/2017/day/13


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_13'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_layers(datalines: list[str]) -> dict[int: int]:
    return {int(line.split(': ')[0]): int(line.split(': ')[1]) for line in datalines}


def draw_layers(
        layers: dict[int: int],
        time: int = None,
        delta: int = 0,
        verbose: bool = False
) -> int | None:
    caught = None


    # header lines
    if verbose:
        print(f'{delta = }')
        print(f'{time = }')
        for col in range(max(layers.keys())+1):
            print(f' {col:03} ', end=' ')
        print()

    # layer lines
    for row in range(max(layers.values())):
        for col in range(max(layers.keys()) + 1):
            if col in layers:
                if layers[col] > row:
                    scan = ' '
                    packet = f'   '
                    if time is not None:
                        r_pos = (time + delta) % (layers[col] * 2 - 2)
                        v_pos = r_pos + (layers[col] - r_pos - 1) * 2 * (r_pos // layers[col])
                        if v_pos == row:
                            scan = 'S'
                        packet = f' {scan} '
                        if row == 0 and time % (max(layers.keys()) + 1) == col:
                            packet = f'({scan})'
                    if verbose:
                        print(f'[{packet}]', end=' ')
                    if packet == '(S)':
                        caught = col
                else:
                    if verbose:
                        print('     ', end=' ')
            else:
                if row == 0:
                    packet = f'.....'
                    if row == 0 and time % (max(layers.keys()) + 1) == col:
                        packet = f'.(.).'
                    if verbose:
                        print(packet, end=' ')
                else:
                    if verbose:
                        print('     ', end=' ')
        if verbose:
            print()

    return caught


test_data = '''
0: 3
1: 2
4: 4
6: 4
'''.strip().splitlines()


@time_it
def main(data_lines: list[str], verbose: bool = False) -> None:
    layers = get_layers(data_lines)
    # pprint(layers)

    severity = 0
    for time in range(max(layers.keys()) + 1):
        caught = draw_layers(layers, time, 0, verbose)
        if caught is not None:
            severity += caught * layers[caught]
        if verbose:
            print('-' * 100)

    print(f'End result: {severity}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # main(data_lines, verbose=True)
    # using test_data:
    #   End result: 24
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 1588
    #   Finished 'main' in 56 milliseconds

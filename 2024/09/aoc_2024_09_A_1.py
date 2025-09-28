# aoc_2024_09_A_1.py - Day 9: Disk Fragmenter - part 1
# Compact the amphipod's hard drive using the process he requested. What is
# the resulting filesystem checksum?
# https://adventofcode.com/2024/day/9


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2024_09'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


# other functions

def decode_map(code: list[str]) -> list[str]:
    result = []
    data = True
    data_id = 0
    for c in code:
        result += ([data_id] if data else '.') * int(c)
        data_id += 1 if data else 0
        data = not data

    return result


def compact_data(data: list[str]) -> list[str]:
    result = [el for el in data]

    dst = 0
    src = len(result) - 1

    while True:
        if result[dst] == '.':
            result[dst], result[src] = result[src], result[dst]
            while result[src] == '.':
                src -= 1
        dst += 1
        if dst >= src:
            break

    return result


def calc_checksum(data: list[str]) -> int:
    return sum(i * (0 if v == '.' else v) for i, v in enumerate(data))


test_data = '''
2333133121414131402
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # print(data_lines[0])

    data = decode_map([c for c in data_lines[0]])
    # print(''.join(str(el) for el in data))

    compacted = compact_data(data)
    # print(''.join(str(el) for el in compacted))

    print(f'End result: {calc_checksum(compacted)}')


if __name__ == "__main__":
    main(load_data(DATA_PATH))
    # main(test_data)

    # using test_data:
    #   End result: 1928
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 6384282079460
    #   Finished 'main' in 52 milliseconds

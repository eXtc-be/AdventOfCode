# aoc_2017_04_A_1.py - Day 4: High-Entropy Passphrases - part 1
# How many passphrases are valid?
# https://adventofcode.com/2017/day/4


from tools import time_it

# other imports

from pprint import pprint


DATA_PATH = './input_2017_04'

# other constants


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def no_doubles(passphrase: str) -> bool:
    return not any(passphrase.split().count(word) > 1 for word in passphrase.split())


test_data = '''
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, validate_passphrase(line))

    valid_passphrases = [phrase for phrase in data_lines if no_doubles(phrase)]

    print(f'End result: {len(valid_passphrases)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 451
    #   Finished 'main' in 3 milliseconds

# aoc_2017_04_B_1.py - Day 4: High-Entropy Passphrases - part 2
# How many passphrases are valid?
# https://adventofcode.com/2017/day/4


from aoc_2017_04_A_1 import (
    DATA_PATH,
    load_data,
    # test_data,
)

from tools import time_it

# other imports

from pprint import pprint


# other constants


def no_anagrams(passphrase: str) -> bool:
    sorted_words = [sorted(word) for word in passphrase.split()]
    return not any(sorted_words.count(word) > 1 for word in sorted_words)


test_data = '''
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    # for line in data_lines:
    #     print(line, no_anagrams(line))

    valid_passphrases = [phrase for phrase in data_lines if no_anagrams(phrase)]

    print(f'End result: {len(valid_passphrases)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 223
    #   Finished 'main' in 3 milliseconds
